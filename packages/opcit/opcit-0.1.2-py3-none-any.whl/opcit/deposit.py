import asyncio
import datetime
import io
import re
from importlib import import_module
from pathlib import Path

from clannotation.annotator import Annotator
import httpx
import lxml
from fastapi import HTTPException, Request, Response, UploadFile
from httpx import Response as HTTPXResponse
from lxml import etree
from lxml.etree import Element

import settings


class OpCit:
    def __init__(
        self,
        request: Request,
        instrumentation=None,
    ):
        self.request = request
        self.instrumentation = instrumentation
        self.namespace = ""

    @staticmethod
    def schema_error():
        """
        Return a Crossref validation error when the schema is not found
        :return: an XML string
        """
        response = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<doi_batch_diagnostic status="completed" sp="cskAir.local">'
            '<record_diagnostic status="Failure" msg_id="4">'
            f"<msg>Record not processed because submitted XML does not match "
            f'any supported schema. Op Cit only supports 5.3.1"</msg>'
            "</record_diagnostic>"
            "<batch_data>"
            "<record_count>1</record_count>"
            "<success_count>0</success_count>"
            "<warning_count>0</warning_count>"
            "<failure_count>1</failure_count>"
            "</batch_data>"
            "</doi_batch_diagnostic>"
        )

        return response

    @staticmethod
    async def determine_successful_deposits(xml_response) -> list[str]:
        """
        Read back the XML response and return a list of DOIs that have been
        processed successfully.
        :param xml_response: the XML response from the live API.
        :return: a list of DOIs that have been processed successfully.
        """
        valid_statuses = {"Success", "Warning"}
        from lxml import etree

        try:
            parser = etree.XMLParser(recover=True)
            root = etree.fromstring(xml_response, parser=parser)

            dois = []
            for record_diagnostic in root.findall(".//record_diagnostic"):
                status = record_diagnostic.get("status")

                doi_element = (
                    record_diagnostic.find("doi")
                    if status in valid_statuses
                    else None
                )
                if doi_element is not None:
                    dois.append(doi_element.text)

            return dois
        except etree.XMLSyntaxError:
            return []

    async def submit_and_validate(
        self, file, login_id, login_password, request: Request, xml_io
    ):
        """
        Submit the XML to the live DOI registration service
        :param file: the file to submit
        :param login_id: the login ID
        :param login_password: the login password
        :param request: the Starlette request object
        :param xml_io: the XML IO object
        :return:
        """
        uf = {"mdFile": (file.filename, xml_io)}

        # submit the XML to the live DOI registration service
        response: HTTPXResponse = await self.proxy_deposit(
            request=request,
            files=uf,
            login_id=login_id,
            login_passwd=login_password,
        )

        response_body = await response.aread()

        # determine which deposits succeeded
        successful_deposits = await self.determine_successful_deposits(
            xml_response=response_body
        )

        return response, response_body, successful_deposits

    async def proxy_deposit(
        self, request: Request, files, login_id, login_passwd
    ) -> Response:
        """
        Send a deposit to the live API
        :param request: the request object
        :param files: the files to deposit
        :param login_id: the login credential
        :param login_passwd: the login password
        :return: httpx Response object
        """
        client = httpx.AsyncClient(
            base_url="https://doi.crossref.org/v2/", timeout=30
        )

        url = httpx.URL(
            path="deposits", query=request.url.query.encode("utf-8")
        )

        mut_headers = request.headers.mutablecopy()
        del mut_headers["content-length"]

        data = {
            "login_id": login_id,
            "login_passwd": login_passwd,
            "operation": "doMDUpload",
        }

        req = client.build_request(
            request.method,
            url,
            headers=mut_headers.raw,
            data=data,
            files=files,
        )

        self.log(f"Sending deposit request to {url}")

        r = await client.send(req, stream=True)

        self.log("Deposit request sent")

        return r

    async def _extract_and_validate_request(self):
        """
        Extract file, login_id, and login_password, and validate the request
        :return: a tuple of the file, login_id, login_password, etree_parsed
            and namespace
        """
        # extract the details and make sure they are a valid Crossref metadata
        # deposit request
        file, login_id, login_password = await self._validate_request(
            self.request
        )

        self.log("Request validated")

        etree_parsed, namespace = self._etree_and_namespace(file)

        (
            etree_object,
            is_valid,
            etree_parsed,
        ) = self._validate_xml_against_schema(parsed_xml=etree_parsed)

        if not is_valid:
            self.log(
                "Invalid XML submitted (does not conform to a "
                "supported Crossref schema)"
            )
            return (
                False,
                file,
                login_id,
                login_password,
                etree_parsed,
                namespace,
            )

        # if we get here, then the document is valid
        self.log("XML is valid Crossref schema")
        return True, file, login_id, login_password, etree_parsed, namespace

    async def _process_dois(self, etree_parsed, warnings) -> dict[str, Element]:
        """
        Process the DOIs in the XML
        :param etree_parsed: the parsed XML
        :param warnings: the warnings list
        :return: a dictionary of DOIs to journal articles
        """
        dois: list[Element] = await self._extract_dois(etree_parsed)
        self.log(f"Found {len(dois)} DOIs for processing")

        dois_to_journal_articles = {}

        for doi in dois:
            # first, find the parent journal_article element
            journal_article: Element = doi.getparent()

            # walk up the tree until we find the journal_article element
            while (
                journal_article is not None
                and not journal_article.tag.endswith("journal_article")
            ):
                journal_article: Element = journal_article.getparent()

                if journal_article is None:
                    break

            if journal_article is None:
                # top of the tree
                # error out
                self.log(f"{doi.text} is not a journal DOI")
                warnings.append(f"{doi.text} is not a journal DOI")
                continue
            else:
                self.log(f"Found journal article for {doi.text}")
                dois_to_journal_articles[doi.text] = journal_article

        return dois_to_journal_articles

    async def _extract_fields(self, journal_article, doi, warnings) -> tuple:
        """
        Extract the fields from the journal article
        :param journal_article: the journal article
        :param doi: the DOI
        :param warnings: the warnings list
        :return: a tuple of fields
        """
        # now look for open licensing information
        license_ref, license_regex = await self._extract_license(
            journal_article
        )

        is_cc = False

        # Extract the text content of the found license_ref
        if (
            license_ref
            and re.match(license_regex, license_ref[0].text) is not None
        ):
            self.log("License is a valid CC license")
            is_cc = True

            resource = await self._extract_fulltext(journal_article)

            if len(resource) > 0:
                remote_file = resource[0].text

                try:
                    self.log(f"Fetching {remote_file}")
                    file_object = await self._fetch_url(url=remote_file)
                except Exception as e:
                    message = (
                        f"Error fetching {remote_file}: {e}. "
                        "This item will not be archived."
                    )
                    self.log(message)
                    warnings.append(message)
                    file_object = None

                if file_object:
                    # extract authors
                    authors = await self._extract_authors(
                        journal_article, namespace=self.namespace
                    )

                    # extract the title
                    title = await self._extract_title(
                        journal_article, namespace=self.namespace
                    )

                    # extract the date
                    date = await self._extract_date(
                        journal_article, namespace=self.namespace
                    )
                else:
                    authors = None
                    title = None
                    date = None
                    resource = None
            else:
                message = (
                    f"No full text resource found for {doi}. "
                    "This item will not be archived."
                )

                self.log(message)
                warnings.append(message)

                file_object = None
                authors = None
                title = None
                date = None
                resource = None
        else:
            message = f"No valid CC license found for {doi}."

            self.log(message)
            warnings.append(message)

            file_object = None
            authors = None
            title = None
            date = None
            resource = None

        return (
            license_ref,
            license_regex,
            is_cc,
            resource,
            authors,
            title,
            date,
            file_object,
        )

    async def process(self) -> Response:
        """
        Process the deposit request
        :return: a Starlette Response object
        """
        warnings = []

        (
            valid,
            file,
            login_id,
            login_password,
            etree_parsed,
            namespace,
        ) = await self._extract_and_validate_request()

        if not valid:
            return Response(
                content=self.schema_error(),
                status_code=400,
            )

        # now look for DOIs
        dois_to_journal_articles = await self._process_dois(
            etree_parsed, warnings
        )

        for doi, journal_article in dois_to_journal_articles.items():
            # extract all fields from the journal article
            (
                license_ref,
                license_regex,
                is_cc,
                resource,
                authors,
                title,
                date,
                file_object,
            ) = await self._extract_fields(journal_article, doi, warnings)

            if is_cc and file_object:
                # deposit in archives
                for (
                    depositor_name,
                    depositor_module,
                ) in settings.Settings.DEPOSIT_SYSTEMS.items():
                    warnings, output = self.deposit(
                        depositor_name=depositor_name,
                        depositor_module=depositor_module,
                        file_object=file_object[0],
                        warnings=warnings,
                        doi=doi,
                        authors=authors,
                        title=title,
                        date=date,
                    )

                    # modify the journal article to point to the Op Cit resource
                    # and generate the resource JSON
                    return_json, md5_doi = await self._build_resource(
                        doi=doi,
                        output=output,
                        journal_article=journal_article,
                        title=title,
                        date=date,
                        full_tree=etree_parsed,
                    )

                    # push the JSON to S3
                    self.instrumentation.aws_connector.push_json_to_s3(
                        json_obj=return_json,
                        path=f"opcit/works/{md5_doi}.json",
                        bucket=settings.Settings.BUCKET,
                    )

                    self.instrumentation.logger.info(
                        f"Pushed {md5_doi} to S3 at opcit/works/{md5_doi}.json"
                    )

        print(etree.tostring(etree_parsed))

        # wrap a bytesio around etree_parsed
        xml_io = io.BytesIO(etree.tostring(etree_parsed))

        # deposit the XML in the Crossref API
        (
            response,
            response_body,
            successful_deposits,
        ) = await self.submit_and_validate(
            file=file,
            login_id=login_id,
            login_password=login_password,
            request=self.request,
            xml_io=xml_io,
        )

        response = Response(content=response_body)
        return response

    @staticmethod
    async def _generate_url(doi) -> (str, str):
        """
        Generate an OpCit URL from a DOI
        :param doi: the DOI from which to generate a URL
        :return: the URL
        """

        md5_doi = Annotator.doi_to_md5(doi)

        return f"https://api.labs.crossref.org/" f"opcit/{md5_doi}", md5_doi

    @staticmethod
    async def _build_resource(
        doi, output, journal_article, title, date, full_tree, namespace="5.3.1"
    ):
        return_json = {
            "doi": doi,
            "title": title,
            "resources": [output],
            "date": date.isoformat(),
        }

        # find all resources in the journal article

        resources = journal_article.xpath(
            "xmlns:doi_data/xmlns:resource",
            namespaces={"xmlns": f"http://www.crossref.org/schema/{namespace}"},
        )

        md5_doi = None

        for resource in resources:
            if resource.text not in return_json["resources"]:
                return_json["resources"].append(resource.text)
                resource.text, md5_doi = await OpCit._generate_url(doi)

        # see if we can find journal metadata in the parent element

        publication_title = full_tree.xpath(
            "//xmlns:journal_metadata/xmlns:full_title",
            namespaces={"xmlns": f"http://www.crossref.org/schema/{namespace}"},
        )

        return_json["publication_title"] = (
            publication_title[0].text if len(publication_title) > 0 else ""
        )

        return return_json, md5_doi

    @staticmethod
    async def _extract_date(
        journal_article, namespace="5.3.1"
    ) -> datetime.date:
        """
        Extract the date from the XML
        :param journal_article: the journal article
        :return: the date object
        """
        date_block: list[Element] = journal_article.xpath(
            ".//publication_date",
            namespaces={"xmlns": f"http://www.crossref.org/schema/{namespace}"},
        )

        date_object = datetime.date(
            year=int(
                journal_article.xpath(
                    ".//xmlns:publication_date/xmlns:year",
                    namespaces={
                        "xmlns": f"http://www.crossref.org/schema/{namespace}"
                    },
                )[0].text
            ),
            month=int(
                journal_article.xpath(
                    ".//xmlns:publication_date/xmlns:month",
                    namespaces={
                        "xmlns": f"http://www.crossref.org/schema/{namespace}"
                    },
                )[0].text
            ),
            day=int(
                journal_article.xpath(
                    ".//xmlns:publication_date/xmlns:day",
                    namespaces={
                        "xmlns": f"http://www.crossref.org/schema/{namespace}"
                    },
                )[0].text
            ),
        )

        return date_object

    @staticmethod
    async def _extract_title(journal_article, namespace="5.3.1") -> str:
        """
        Extract the title from the XML
        :param journal_article: the journal article
        :return: the title text
        """
        titles: list[Element] = journal_article.xpath(
            ".//xmlns:titles/xmlns:title",
            namespaces={"xmlns": f"http://www.crossref.org/schema/{namespace}"},
        )

        return titles[0].text

    @staticmethod
    async def _extract_authors(journal_article, namespace="5.3.1") -> list[str]:
        """
        Extract the authors from the XML
        :param journal_article: the journal article
        :return: a list of authors in FirstName LastName format
        """
        contributors: list[Element] = journal_article.xpath(
            ".//xmlns:contributors/*[@contributor_role = 'author']",
            namespaces={"xmlns": f"http://www.crossref.org/schema/{namespace}"},
        )

        authors = []

        for contributor in contributors:
            if contributor.tag.endswith("person_name"):
                author = {
                    "given_name": contributor.xpath(
                        ".//xmlns:given_name",
                        namespaces={
                            "xmlns": f"http://www.crossref.org/schema/{namespace}"
                        },
                    )[0].text,
                    "surname": contributor.xpath(
                        ".//xmlns:surname",
                        namespaces={
                            "xmlns": f"http://www.crossref.org/schema/{namespace}"
                        },
                    )[0].text,
                }

                is_first = contributor.xpath(
                    ".//@sequence[.='first']",
                    namespaces={
                        "xmlns": f"http://www.crossref.org/schema/{namespace}"
                    },
                )

                authenticated_orcid = contributor.xpath(
                    ".//xmlns:ORCID[@authenticated='true']",
                    namespaces={
                        "xmlns": f"http://www.crossref.org/schema/{namespace}"
                    },
                )

                if authenticated_orcid:
                    author["ORCID"] = authenticated_orcid[0].text

                if is_first:
                    authors.insert(
                        0, author["given_name"] + " " + author["surname"]
                    )
                else:
                    authors.append(
                        author["given_name"] + " " + author["surname"]
                    )

        return authors

    @staticmethod
    async def _extract_fulltext(journal_article, namespace="5.3.1"):
        """
        Extract the full text resource URL from the XML
        :param journal_article: the journal article element
        :return: a list of resource elements
        """
        resource: list[Element] = journal_article.xpath(
            './/xmlns:collection[@property="crawler-based"]/xmlns:item'
            '[@crawler="iParadigms"]/xmlns:resource',
            namespaces={"xmlns": f"http://www.crossref.org/schema/{namespace}"},
        )
        return resource

    @staticmethod
    async def _extract_license(journal_article):
        """
        Extract the license from the XML
        :param journal_article: the journal article
        :return: the license_ref element and the license_regex for matching
        """
        # this extracts license elements of the kind:
        # <license_ref applies_to="vor" start_date="2008-08-13">
        # http://creativecommons.org/licenses/by/3.0/deed.en_US</license_ref>

        license_regex = r"^https?://creativecommons.org/licenses/.+"
        license_element = "license_ref"
        necessary_applies_to = "vor"
        license_ref = journal_article.xpath(
            f'//xmlns:{license_element}[@applies_to="'
            f'{necessary_applies_to}"]',
            namespaces={
                "xmlns": "http://www.crossref.org/AccessIndicators.xsd"
            },
        )
        return license_ref, license_regex

    @staticmethod
    async def _extract_dois(parsed_xml) -> list[Element]:
        """
        Extract the DOIs from the XML
        :param parsed_xml: the parsed XML
        :return: a list of DOI elements
        """
        crossref_namespace = OpCit._extract_namespace(parsed_xml)
        namespaces = {"crossref": crossref_namespace}

        doi_data_elements = parsed_xml.findall(
            f".//crossref:doi_data/crossref:doi", namespaces=namespaces
        )
        return doi_data_elements

    def deposit(
        self,
        depositor_name,
        depositor_module,
        file_object,
        warnings: list,
        doi,
        authors,
        title,
        date,
    ) -> tuple[list, str]:
        """
        Deposit a file in an archive
        :param doi: the DOI
        :param warnings: the warnings list
        :param depositor_name: the name
        :param depositor_module: depositor module string
        :param file_object: the file object to deposit
        :param authors: the authors
        :param date: the item's date
        :return: a list of warnings and an output location string
        """
        self.log(f"Loading module {depositor_name}")
        process_module = import_module(f"depositors.{depositor_module}")

        # build a metadata dictionary
        metadata = {
            "title": title,
            "authors": authors,
            "date": date,
            "doi": doi,
        }

        archive = process_module.Archive(self.log)
        warnings, output = archive.deposit(
            file_object=file_object,
            warnings=warnings,
            doi=doi,
            metadata=metadata,
        )

        self.log(f"Deposited {doi} to {depositor_name} at {output}")

        return warnings, output

    def log(self, message) -> None:
        """
        Log a message
        :param message: the message to log
        :return: None
        """
        if self.instrumentation:
            self.instrumentation.logger.info(message)

    @staticmethod
    async def _make_request(client: httpx.AsyncClient, url: str) -> bytes:
        """
        Make a remote request
        :param client: the client object
        :param url: the URL to request
        :return: the response
        """
        response = await client.get(url)

        return response.content

    @staticmethod
    async def _fetch_url(url) -> tuple[bytes]:
        """
        Fetch a remote URL
        :param url: the URL to fetch
        :return: list of async task responses
        """
        async with httpx.AsyncClient() as client:
            tasks = [OpCit._make_request(client, url)]
            result = await asyncio.gather(*tasks)
            return result

    @staticmethod
    async def _validate_request(request) -> tuple[UploadFile, str, str]:
        """
        Check that this is a valid deposit request and extract the needed info
        :param request: the current request
        :return: a tuple of the submitted file, login_id, and login_passwd
        """
        # 1. check that the content type of this request is
        #  "multipart/form-data"
        # 2. check that the following parameters are all set:
        # a. login_id, the depositing username and/or role in format user/role
        #  or role
        # b. login_passwd, the depositing user password
        # c. operation, the value should be “doMDUpload”.
        # 3. extract the file from the request (in the "files" parameter)

        content_type = request.headers.get("content-type")
        if content_type.startswith("multipart/form-data"):
            form = await request.form()

            if (
                "login_id" in form
                and "login_passwd" in form
                and "operation" in form
            ):
                if form["operation"] == "doMDUpload":
                    if "mdFile" in form:
                        return (
                            form["mdFile"],
                            form["login_id"],
                            form["login_passwd"],
                        )
                    else:
                        raise HTTPException(
                            status_code=400,
                            detail="Missing 'mdFile' field in the request.",
                        )
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid value for 'operation'. "
                        "Must be 'doMDUpload'.",
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Missing required parameters "
                    "(login_id, login_passwd, operation).",
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid content type. Must be 'multipart/form-data'.",
            )

    def _validate_xml_against_schema(
        self,
        parsed_xml,
        base_url="",
        reload=False,
    ) -> tuple[etree, bool, etree]:
        """
        Validate the XML against the schema
        :param parsed_xml: the parsed XML
        :param base_url: the base URL
        :param reload: whether to reload the XML
        :return: tuple of etree, is_valid, parsed_xml
        """

        if isinstance(parsed_xml, lxml.etree._ElementTree):
            root = parsed_xml.getroot()
        else:
            root = parsed_xml

        schema_location = root.get(
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"
        )
        regex = r"^http://www.crossref.org/schema/(.+) "

        match = re.search(regex, schema_location)

        if match:
            capturing_group = match.group(1)
        else:
            return etree, False, parsed_xml

        self.namespace = match.group(1)

        xsd_file = Path(
            f"depositor_schema/{capturing_group}/crossref{capturing_group}.xsd"
        )

        xml_element_tree = parsed_xml

        if not xsd_file.exists():
            return etree, False, None

        if base_url:
            xsd_tree = etree.parse(
                xsd_file, base_url=base_url if base_url else None
            )
        else:
            xsd_tree = etree.parse(xsd_file)

        if reload:
            # reparse
            xml_element_tree = etree.fromstring(
                etree.tostring(xml_element_tree)
            )

        xml_schema = etree.XMLSchema(xsd_tree)
        is_valid = xml_schema.validate(xml_element_tree)

        return etree, is_valid, parsed_xml

    def _etree_and_namespace(self, file) -> tuple[etree, str]:
        """
        Parse the XML and extract the namespace
        :param file: the file to parse
        :return: tuple of etree and namespace
        """
        # validate the XML against the schema
        from lxml import etree

        parsed_xml = etree.parse(file.file)

        return parsed_xml, self._extract_namespace(parsed_xml)

    @staticmethod
    def _extract_namespace(
        tree, namespace: str = None, namespace_mode=False
    ) -> str:
        """
        Extract the namespace from an XML tree.
        :param tree: the XML tree
        :param namespace: the namespace or None
        :param namespace_mode: whether to return the namespace or the URL
        :return: the namespace
        """

        if namespace is None:
            return tree.xpath(f"namespace-uri(.)")

        else:
            ns_select = (
                "//namespace::*[not(. = "
                "'http://www.w3.org/XML/1998/namespace') "
                "and . = namespace-uri(..)]"
            )

            for ns, url in tree.xpath(ns_select):
                if not namespace_mode:
                    if ns == namespace:
                        return url
                else:
                    if url == namespace:
                        return ns
