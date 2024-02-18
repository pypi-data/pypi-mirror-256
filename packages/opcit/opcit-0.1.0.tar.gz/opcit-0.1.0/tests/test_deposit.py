import datetime
import io
import sys
import unittest
from pathlib import Path
from string import Template
from typing import BinaryIO
from unittest.mock import MagicMock, patch, Mock, AsyncMock

import httpx
import lxml
from fastapi import HTTPException, UploadFile
from httpx import Response
from lxml import etree
from starlette.datastructures import FormData
from starlette.requests import Request


class TestProcessDOIs(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    async def test_process_dois(self):
        xml_content = """
            <doi_batch xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://www.crossref.org/schema/5.3.1 https://www.crossref.org/schemas/crossref5.3.1.xsd"
                xmlns="http://www.crossref.org/schema/5.3.1" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
                xmlns:fr="http://www.crossref.org/fundref.xsd" version="5.3.1">
                <head>
                    <doi_batch_id>test.x</doi_batch_id>
                    <timestamp>${timestamp}</timestamp>
                    <depositor>
                        <depositor_name>Crossref</depositor_name>
                        <email_address>pfeeney@crossref.org</email_address>
                    </depositor>
                    <registrant>Society of Metadata Idealists</registrant>
                </head>
                <body>
                    <journal>
                        <journal_metadata language="en">
                            <full_title>Journal of Metadata Perfection</full_title>
                            <abbrev_title>JOMPer</abbrev_title>
                            <doi_data>
                                <doi>10.32013/487529</doi>
                                <resource>https://www.crossref.org/jomper</resource>
                            </doi_data>
                        </journal_metadata>
                        
                        <journal_article publication_type="full_text">
                            <titles>
                                <title>Why 'blah blah blah dah' is the second best test data title</title>
                            </titles>
                            <contributors>
                                <person_name sequence="first" contributor_role="author">
                                    <given_name>Minerva</given_name>
                                    <surname>Housecat</surname>
                                    <affiliations>
                                        <institution>
                                            <institution_id type="ror">https://ror.org/05gq02987</institution_id>
                                        </institution>
                                    </affiliations>
                                    <ORCID authenticated="true">https://orcid.org/0000-0002-4011-3590</ORCID>
                                </person_name>
                                <person_name sequence="additional" contributor_role="author">
                                    <given_name>Eve</given_name>
                                    <surname>Martin Paul</surname>
                                    <affiliations>
                                        <institution>
                                            <institution_id type="ror">https://ror.org/02mb95055</institution_id>
                                        </institution>
                                    </affiliations>
                                    <ORCID authenticated="true">https://orcid.org/0000-0002-5589-8511</ORCID>
                                </person_name>
                            </contributors>
                            <jats:abstract>
                                <jats:p>Agile
                                    best practices, thought leadership collective impact impact investing to
                                    families. And equal opportunity vibrant, the, storytelling synergy metadata
                                    matters B-corp unprecedented challenge. Venture philanthropy cultivate
                                    impact, state of play; white paper collaborative consumption entrepreneur
                                    collaborative cities inclusive. Parse empower communities movements
                                    targeted; radical; social enterprise issue outcomes big data venture
                                    philanthropy. </jats:p>
                            </jats:abstract>
                            <publication_date media_type="online">
                                <month>01</month>
                                <day>01</day>
                                <year>2022</year>
                            </publication_date>
                            <acceptance_date>
                                <month>05</month>
                                <day>21</day>
                                <year>2021</year>
                            </acceptance_date>
                                    <!-- CC BY license -->
                                    <program xmlns="http://www.crossref.org/AccessIndicators.xsd">
                                        <free_to_read/>
                                        <license_ref applies_to="tdm" start_date="2022-01-01"
                                            >https://creativecommons.org/licenses/by/4.0/</license_ref>
                                        <license_ref applies_to="vor" start_date="2022-01-01">https://creativecommons.org/licenses/by/4.0/</license_ref>
                                    </program>
            
                            <doi_data>
                                <doi>10.32013/123456789-23</doi>
                                <resource content_version="vor">https://www.crossref.org/xml-samples/</resource>
                                <!-- PDF URL for similarity check -->
                                <collection property="crawler-based">
                                    <item crawler="iParadigms">
                                        <resource mime_type="application/pdf">https://eprintsds.bbk.ac.uk/id/eprint/26645/1/9780198850489.pdf</resource>
                                    </item>
                                </collection>
                                <collection property="text-mining">
                                    <item>
                                        <resource content_version="vor" mime_type="text/xml"
                                            >https://www.crossref.org/example.xml</resource>
                                    </item>
                                </collection>
                            </doi_data>
                        </journal_article>
                    </journal>
                </body>
            </doi_batch>
        """

        # Create an Element object from the XML content
        etree_parsed = etree.fromstring(xml_content)

        from opcit.opcit import deposit

        instance = deposit.OpCit(request=Request(scope={"type": "http"}))

        warnings = []
        result = await instance._process_dois(etree_parsed, warnings)

        self.assertIsInstance(
            result["10.32013/123456789-23"], lxml.etree._Element
        )

    async def test_process_dois_no_journal_articles(self):
        xml_content = """
                    <doi_batch xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                        xsi:schemaLocation="http://www.crossref.org/schema/5.3.1 https://www.crossref.org/schemas/crossref5.3.1.xsd"
                        xmlns="http://www.crossref.org/schema/5.3.1" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
                        xmlns:fr="http://www.crossref.org/fundref.xsd" version="5.3.1">
                        <head>
                            <doi_batch_id>test.x</doi_batch_id>
                            <timestamp>${timestamp}</timestamp>
                            <depositor>
                                <depositor_name>Crossref</depositor_name>
                                <email_address>pfeeney@crossref.org</email_address>
                            </depositor>
                            <registrant>Society of Metadata Idealists</registrant>
                        </head>
                        <body>
                            <journal>
                                <journal_metadata language="en">
                                    <full_title>Journal of Metadata Perfection</full_title>
                                    <abbrev_title>JOMPer</abbrev_title>
                                    <doi_data>
                                        <doi>10.32013/487529</doi>
                                        <resource>https://www.crossref.org/jomper</resource>
                                    </doi_data>
                                </journal_metadata>
                            </journal>
                        </body>
                    </doi_batch>
                """

        # Create an Element object from the XML content
        etree_parsed = etree.fromstring(xml_content)

        from opcit.opcit import deposit

        instance = deposit.OpCit(request=Request(scope={"type": "http"}))

        warnings = []
        result = await instance._process_dois(etree_parsed, warnings)

        self.assertEqual(result, {})


class TestExtractFields(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    async def test_extract_fields_with_license_and_no_resource(self):
        # Mock the dependencies of the function
        mock_license_ref = MagicMock()
        mock_license_ref.text = "https://creativecommons.org/licenses/by/4.0/"
        mock_license_regex = r"^https?://creativecommons.org/licenses/.+"
        mock_extract_license = AsyncMock(
            return_value=([mock_license_ref], mock_license_regex)
        )

        mock_fulltext_element = MagicMock()
        mock_fulltext_element.text = "https://example.com/fulltext.pdf"
        mock_extract_fulltext = AsyncMock(return_value=[mock_fulltext_element])

        mock_fetch_url = AsyncMock(return_value=b"File content")
        mock_fetch_url.side_effect = HTTPException(
            status_code=404, detail="Fulltext resource not found"
        )

        mock_extract_authors = AsyncMock(return_value=["Author 1", "Author 2"])
        mock_extract_title = AsyncMock(return_value="Title")
        mock_extract_date = AsyncMock(return_value="2022-01-01")

        # Set up the mock instance of YourClass
        from opcit.opcit import deposit

        instance = deposit.OpCit(request=Request(scope={"type": "http"}))

        instance._extract_license = mock_extract_license
        instance._extract_fulltext = mock_extract_fulltext
        instance._fetch_url = mock_fetch_url
        instance._extract_authors = mock_extract_authors
        instance._extract_title = mock_extract_title
        instance._extract_date = mock_extract_date

        # Call the extract_fields function
        journal_article = MagicMock()
        doi = "example_doi"
        warnings = []

        result = await instance._extract_fields(journal_article, doi, warnings)

        # Assert the function calls and the result
        mock_extract_license.assert_awaited_once_with(journal_article)
        mock_extract_fulltext.assert_awaited_once_with(journal_article)
        mock_fetch_url.assert_awaited_once_with(
            url="https://example.com/fulltext.pdf"
        )
        mock_extract_authors.assert_not_called()
        mock_extract_title.assert_not_called()
        mock_extract_date.assert_not_called()

        expected_result = (
            [mock_license_ref],
            mock_license_regex,
            True,
            None,
            None,
            None,
            None,
            None,
        )
        self.assertEqual(result, expected_result)

    async def test_extract_fields_with_license_and_resource(self):
        # Mock the dependencies of the function
        mock_license_ref = MagicMock()
        mock_license_ref.text = "https://creativecommons.org/licenses/by/4.0/"
        mock_license_regex = r"^https?://creativecommons.org/licenses/.+"
        mock_extract_license = AsyncMock(
            return_value=([mock_license_ref], mock_license_regex)
        )

        mock_fulltext_element = MagicMock()
        mock_fulltext_element.text = "https://example.com/fulltext.pdf"
        mock_extract_fulltext = AsyncMock(return_value=[mock_fulltext_element])

        mock_fetch_url = AsyncMock(return_value=b"File content")

        mock_extract_authors = AsyncMock(return_value=["Author 1", "Author 2"])
        mock_extract_title = AsyncMock(return_value="Title")
        mock_extract_date = AsyncMock(return_value="2022-01-01")

        # Set up the mock instance of YourClass
        from opcit.opcit import deposit

        instance = deposit.OpCit(request=Request(scope={"type": "http"}))

        instance._extract_license = mock_extract_license
        instance._extract_fulltext = mock_extract_fulltext
        instance._fetch_url = mock_fetch_url
        instance._extract_authors = mock_extract_authors
        instance._extract_title = mock_extract_title
        instance._extract_date = mock_extract_date

        # Call the extract_fields function
        journal_article = MagicMock()
        doi = "example_doi"
        warnings = []

        result = await instance._extract_fields(journal_article, doi, warnings)

        # Assert the function calls and the result
        expected_result = (
            [mock_license_ref],
            mock_license_regex,
            True,
            [mock_fulltext_element],
            ["Author 1", "Author 2"],
            "Title",
            "2022-01-01",
            b"File content",
        )
        self.assertEqual(result, expected_result)

    async def test_extract_fields_with_no_license_and_resource(self):
        # Mock the dependencies of the function
        mock_license_ref = MagicMock()
        mock_license_ref.text = "All Rights Reserved"
        mock_license_regex = r"^https?://creativecommons.org/licenses/.+"
        mock_extract_license = AsyncMock(
            return_value=([mock_license_ref], mock_license_regex)
        )

        mock_fulltext_element = MagicMock()
        mock_fulltext_element.text = "https://example.com/fulltext.pdf"
        mock_extract_fulltext = AsyncMock(return_value=[mock_fulltext_element])

        mock_fetch_url = AsyncMock(return_value=b"File content")

        mock_extract_authors = AsyncMock(return_value=["Author 1", "Author 2"])
        mock_extract_title = AsyncMock(return_value="Title")
        mock_extract_date = AsyncMock(return_value="2022-01-01")

        # Set up the mock instance of YourClass
        from opcit.opcit import deposit

        instance = deposit.OpCit(request=Request(scope={"type": "http"}))

        instance._extract_license = mock_extract_license
        instance._extract_fulltext = mock_extract_fulltext
        instance._fetch_url = mock_fetch_url
        instance._extract_authors = mock_extract_authors
        instance._extract_title = mock_extract_title
        instance._extract_date = mock_extract_date

        # Call the extract_fields function
        journal_article = MagicMock()
        doi = "example_doi"
        warnings = []

        result = await instance._extract_fields(journal_article, doi, warnings)

        # Assert the function calls and the result
        mock_extract_license.assert_awaited_once_with(journal_article)
        mock_extract_fulltext.assert_not_called()
        mock_fetch_url.assert_not_called()

        mock_extract_authors.assert_not_called()
        mock_extract_title.assert_not_called()
        mock_extract_date.assert_not_called()

        expected_result = (
            [mock_license_ref],
            mock_license_regex,
            False,
            None,
            None,
            None,
            None,
            None,
        )
        self.assertEqual(result, expected_result)


class TestExtractAndValidateRequest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    @patch("opcit.opcit.deposit.OpCit._validate_request")
    @patch("opcit.opcit.deposit.OpCit._etree_and_namespace")
    @patch("opcit.opcit.deposit.OpCit._validate_xml_against_schema")
    async def test_extract_and_validate_request_valid(
        self, mock_validate_xml, mock_etree_and_namespace, mock_validate_request
    ):
        # Mock the necessary methods to simulate a valid request
        mock_file = MagicMock()
        mock_login_id = "user/role"
        mock_login_password = "password"
        mock_etree_parsed = MagicMock()
        mock_namespace = "http://www.crossref.org/schema/5.3.1"

        mock_validate_request.return_value = (
            mock_file,
            mock_login_id,
            mock_login_password,
        )
        mock_etree_and_namespace.return_value = (
            mock_etree_parsed,
            mock_namespace,
        )
        mock_validate_xml.return_value = (None, True, None)

        from opcit.opcit import deposit

        instance = deposit.OpCit(request=Request(scope={"type": "http"}))

        # Call the _extract_and_validate_request method
        result = await instance._extract_and_validate_request()

        # Assert that the result is a tuple with the expected values
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)
        self.assertTrue(result[0])  # Should be True for a valid request

    @patch("opcit.opcit.deposit.OpCit._validate_request")
    @patch("opcit.opcit.deposit.OpCit._etree_and_namespace")
    @patch("opcit.opcit.deposit.OpCit._validate_xml_against_schema")
    async def test_extract_and_validate_request_invalid_xml(
        self, mock_validate_xml, mock_etree_and_namespace, mock_validate_request
    ):
        # Mock the necessary methods to simulate an invalid XML request
        mock_file = MagicMock()
        mock_login_id = "user/role"
        mock_login_password = "password"
        mock_etree_parsed = MagicMock()
        mock_namespace = "http://www.crossref.org/schema/5.3.1"

        mock_validate_request.return_value = (
            mock_file,
            mock_login_id,
            mock_login_password,
        )
        mock_etree_and_namespace.return_value = (
            mock_etree_parsed,
            mock_namespace,
        )
        mock_validate_xml.return_value = (None, False, None)

        from opcit.opcit import deposit

        instance = deposit.OpCit(request=Request(scope={"type": "http"}))

        # Call the _extract_and_validate_request method
        result = await instance._extract_and_validate_request()

        # Assert that the result is a tuple with the expected values
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 6)
        self.assertFalse(result[0])  # Should be False for an invalid XML


class TestDeposit(unittest.TestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    @patch("opcit.opcit.deposit.import_module")
    def test_deposit_success(self, mock_import_module):
        # Mock the import_module to return a mock Archive class
        mock_archive_class = Mock()
        mock_import_module.return_value.Archive = mock_archive_class

        # Mock the deposit method of the Archive class
        mock_archive_instance = mock_archive_class.return_value
        mock_archive_instance.deposit.return_value = (None, None)

        from opcit.opcit import deposit

        instance = deposit.OpCit(request=Request(scope={"type": "http"}))

        # Call the deposit method with mock parameters
        depositor_name = "DepositorName"
        depositor_module = "DepositorModule"
        file_object = b"File content"
        warnings = []
        doi = "example_doi"

        instance.deposit(
            depositor_name=depositor_name,
            depositor_module=depositor_module,
            file_object=file_object,
            warnings=warnings,
            doi=doi,
            authors=[],
            title="",
            date="",
        )

        # Assert that the import_module and deposit methods were called
        mock_import_module.assert_called_once_with(
            f"depositors.{depositor_module}"
        )
        mock_archive_class.assert_called_once_with(instance.log)
        mock_archive_instance.deposit.assert_called_once_with(
            file_object=file_object,
            warnings=warnings,
            doi=doi,
            metadata={
                "authors": [],
                "date": "",
                "doi": "example_doi",
                "title": "",
            },
        )

    @patch("opcit.opcit.deposit.import_module")
    def test_deposit_import_error(self, mock_import_module):
        # Mock the import_module to raise an ImportError
        mock_import_module.side_effect = ImportError("Module not found")

        from opcit.opcit import deposit

        your_instance = deposit.OpCit(request=Request(scope={"type": "http"}))

        # Call the deposit method with mock parameters
        depositor_name = "DepositorName"
        depositor_module = "DepositorModule"
        file_object = b"File content"
        warnings = []
        doi = "example_doi"

        with self.assertRaises(ImportError):
            your_instance.deposit(
                depositor_name=depositor_name,
                depositor_module=depositor_module,
                file_object=file_object,
                warnings=warnings,
                doi=doi,
                authors=[],
                title="",
                date="",
            )


class TestFetchUrl(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    @patch("opcit.opcit.deposit.OpCit._make_request")
    async def test_fetch_url_success(self, mock_make_request):
        # Mock the _make_request function to return a response
        mock_response = Mock(spec=httpx.Response)
        mock_response.content = b"This is the content"
        mock_make_request.return_value = mock_response

        # Call the _fetch_url function with a mock URL
        from opcit.opcit import deposit

        url = "http://example.com"
        result: tuple[bytes] = await deposit.OpCit._fetch_url(url)

        # Assert that the result is a tuple containing bytes
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Response)
        self.assertEqual(result[0].content, b"This is the content")

    @patch("opcit.opcit.deposit.OpCit._make_request")
    async def test_fetch_url_error(self, mock_make_request):
        # Mock the _make_request function to raise an exception
        mock_make_request.side_effect = httpx.RequestError("Error")

        # Call the _fetch_url function with a mock URL
        from opcit.opcit import deposit

        url = "http://example.com"
        result = None
        with self.assertRaises(httpx.RequestError):
            result = await deposit.OpCit._fetch_url(url)

        # Assert that the result is a tuple containing bytes
        self.assertIsNone(result)


class TestValidateXML(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    def test_validate_xml(self):
        # Create an XML tree without a namespace
        # load XML content from test.xml file and template in a timestamp

        import datetime

        current_time = datetime.datetime.now()

        time_stamp = str(current_time.timestamp()).split(".")[0]

        with open(
            "../../test_data/5.3.1.xml",
            "r",
        ) as f:
            xml = Template(f.read())
            xml = xml.substitute(timestamp=time_stamp)

        # Create an Element object from the XML content
        parsed_xml = etree.fromstring(xml.encode("utf-8"))

        # Call the _extract_namespace method without specifying a namespace
        from opcit.opcit import deposit

        opcit_obj = deposit.OpCit(request=Request(scope={"type": "http"}))

        (
            etree_obj,
            result,
            xml_returned,
        ) = opcit_obj._validate_xml_against_schema(parsed_xml)

        self.assertEqual(True, result)


class TestExtract(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    def test_extract_namespace_without_namespace(self):
        # Create an XML tree without a namespace
        xml_content = """
            <root>
                <element>Test</element>
            </root>
        """
        tree = etree.fromstring(xml_content)

        # Call the _extract_namespace method without specifying a namespace
        namespace = self._extract_namespace(tree)
        self.assertEqual(namespace, "")

    def _extract_namespace(self, tree, namespace=None, namespace_mode=False):
        from opcit.opcit import deposit

        # Call the _extract_namespace method
        return deposit.OpCit._extract_namespace(tree, namespace, namespace_mode)

    async def test_extract_title(self):
        # Sample XML content with a title
        xml_content = """
            <journal_article xmlns="http://www.crossref.org/schema/5.3.1">
                <titles>
                    <title>Title of the Article</title>
                </titles>
            </journal_article>
        """

        # Create an Element object from the XML content
        journal_article = etree.fromstring(xml_content)

        # Call the _extract_title method
        title = await self._extract_title(journal_article)

        # Assert that the title is extracted correctly
        self.assertEqual(title, "Title of the Article")

    @staticmethod
    async def _extract_title(journal_article):
        from opcit.opcit import deposit

        # Call the _extract_title method
        return await deposit.OpCit._extract_title(journal_article)

    async def test_extract_date(self):
        # Sample XML content with publication_date
        xml_content = """
            <journal_article xmlns="http://www.crossref.org/schema/5.3.1">
                <publication_date>
                    <year>2023</year>
                    <month>12</month>
                    <day>15</day>
                </publication_date>
            </journal_article>
        """

        # Create an Element object from the XML content
        journal_article = etree.fromstring(xml_content)

        # Call the _extract_date method
        date_object = await self._extract_date(journal_article)

        # Assert date_object is a datetime.date object with the expected date
        self.assertIsInstance(date_object, datetime.date)
        self.assertEqual(date_object, datetime.date(2023, 12, 15))

    @staticmethod
    def _extract_date(journal_article):
        from opcit.opcit import deposit

        # Call the _extract_date method
        return deposit.OpCit._extract_date(journal_article)

    async def test_extract_authors(self):
        # Sample XML content with authors
        xml_content = """
            <journal_article xmlns="http://www.crossref.org/schema/5.3.1">
                <contributors>
                    <person_name contributor_role="author">
                        <given_name>John</given_name>
                        <surname>Doe</surname>
                    </person_name>
                    <person_name contributor_role="author">
                        <given_name>Jane</given_name>
                        <surname>Smith</surname>
                        <ORCID authenticated="true">1234567890</ORCID>
                    </person_name>
                </contributors>
            </journal_article>
        """

        # Create an Element object from the XML content
        journal_article = etree.fromstring(xml_content)

        # Call the _extract_authors method
        authors = await self._extract_authors(journal_article)

        # Assert that authors are extracted correctly
        self.assertEqual(
            ["John Doe", "Jane Smith"],
            authors,
        )

    @staticmethod
    async def _extract_authors(journal_article):
        from opcit.opcit import deposit

        # Call the _extract_authors method
        return await deposit.OpCit._extract_authors(journal_article)

    async def test_extract_fulltext(self):
        # Sample XML content with fulltext resources
        xml_content = """
            <journal_article xmlns="http://www.crossref.org/schema/5.3.1">
                <collection property="crawler-based">
                    <item crawler="iParadigms">
                        <resource>Fulltext Resource 1</resource>
                        <resource>Fulltext Resource 2</resource>
                    </item>
                </collection>
            </journal_article>
        """

        # Create an Element object from the XML content
        journal_article = etree.fromstring(xml_content)

        # Mock the journal_article.xpath method

        resources = await self._extract_fulltext(journal_article)

        self.assertEqual(resources[0].text, "Fulltext Resource 1")
        self.assertEqual(resources[1].text, "Fulltext Resource 2")

    @staticmethod
    async def _extract_fulltext(journal_article):
        from opcit.opcit import deposit

        # Call the _extract_fulltext method
        return await deposit.OpCit._extract_fulltext(journal_article)

    async def test_extract_license(self):
        # Sample XML content with a license_ref element
        xml_content = """
            <journal_article xmlns="http://www.crossref.org/AccessIndicators.xsd">
                <license_ref applies_to="vor" start_date="2008-08-13">
                    http://creativecommons.org/licenses/by/3.0/deed.en_US
                </license_ref>
            </journal_article>
        """

        # Create an Element object from the XML content
        journal_article = etree.fromstring(xml_content)

        # Call the _extract_license method
        license_ref, license_regex = await self._extract_license(
            journal_article
        )

        # Assert that license_ref and license_regex are extracted correctly
        self.assertEqual(
            license_ref[0].text.strip(),
            "http://creativecommons.org/licenses/by/3.0/deed.en_US",
        )
        self.assertEqual(
            license_regex, "^https?://creativecommons.org/licenses/.+"
        )

    @staticmethod
    async def _extract_license(journal_article):
        from opcit.opcit import deposit

        # Call the _extract_license method
        return await deposit.OpCit._extract_license(journal_article)

    async def test_extract_dois(self):
        # Sample XML content with DOI data elements
        xml_content = """
            <doi_batch xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="http://www.crossref.org/schema/5.3.1 https://www.crossref.org/schemas/crossref5.3.1.xsd"
                xmlns="http://www.crossref.org/schema/5.3.1" xmlns:jats="http://www.ncbi.nlm.nih.gov/JATS1"
                xmlns:fr="http://www.crossref.org/fundref.xsd" version="5.3.1">
                <head>
                    <doi_batch_id>test.x</doi_batch_id>
                    <timestamp>${timestamp}</timestamp>
                    <depositor>
                        <depositor_name>Crossref</depositor_name>
                        <email_address>pfeeney@crossref.org</email_address>
                    </depositor>
                    <registrant>Society of Metadata Idealists</registrant>
                </head>
                <body>
                    <journal>
                        <journal_metadata language="en">
                            <full_title>Journal of Metadata Perfection</full_title>
                            <abbrev_title>JOMPer</abbrev_title>
                            <doi_data>
                                <doi>10.32013/487529</doi>
                                <resource>https://www.crossref.org/jomper</resource>
                            </doi_data>
                        </journal_metadata>
                    </journal>
                </body>
            </doi_batch>
        """

        # Create an Element object from the XML content
        parsed_xml = etree.fromstring(xml_content)

        # Call the _extract_dois method
        doi_data_elements = await self._extract_dois(parsed_xml)

        # Assert that doi_data_elements are extracted correctly
        self.assertEqual(len(doi_data_elements), 1)
        self.assertEqual(
            [element.text for element in doi_data_elements],
            ["10.32013/487529"],
        )

    @staticmethod
    async def _extract_dois(parsed_xml):
        from opcit.opcit import deposit

        # Call the _extract_dois method
        return await deposit.OpCit._extract_dois(parsed_xml)


class TestValidateRequest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    @staticmethod
    async def return_form(form):
        return form

    @staticmethod
    def string_to_binary_io(data: str) -> BinaryIO:
        # Encode the string as bytes
        bytes_data = data.encode("utf-8")

        # Create a BinaryIO object using io.BytesIO
        binary_io = io.BytesIO(bytes_data)

        return binary_io

    async def test_valid_request(self):
        # Create a valid request with the required fields
        request = MagicMock()
        request.headers.get.return_value = "multipart/form-data"
        form_data = FormData(
            {
                "login_id": "user/role",
                "login_passwd": "password",
                "operation": "doMDUpload",
                "mdFile": UploadFile(
                    filename="test.txt", file=self.string_to_binary_io("test")
                ),
            },
        )

        request.form.return_value = self.return_form(form_data)

        # Call the _validate_request method
        file, login_id, login_passwd = await self._validate_request(request)

        # Assert that the extracted values are correct
        self.assertIsInstance(file, UploadFile)
        self.assertEqual(login_id, "user/role")
        self.assertEqual(login_passwd, "password")

    async def test_missing_mdFile(self):
        # Create a request with missing 'mdFile' field
        request = MagicMock()
        request.headers.get.return_value = "multipart/form-data"
        form_data = FormData(
            {
                "login_id": "user/role",
                "login_passwd": "password",
                "operation": "doMDUpload",
            },
        )

        request.form.return_value = self.return_form(form_data)

        # Call the _validate_request method and expect an HTTPException
        with self.assertRaises(HTTPException) as context:
            await self._validate_request(request)

        # Assert the expected error message
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(
            context.exception.detail,
            "Missing 'mdFile' field in the request.",
        )

    async def test_invalid_operation(self):
        # Create a request with invalid 'operation' value
        request = MagicMock()
        request.headers.get.return_value = "multipart/form-data"
        form_data = FormData(
            {
                "login_id": "user/role",
                "login_passwd": "password",
                "operation": "Bad Op",
                "mdFile": UploadFile(
                    filename="test.txt", file=self.string_to_binary_io("test")
                ),
            },
        )

        request.form.return_value = self.return_form(form_data)

        # Call the _validate_request method and expect an HTTPException
        with self.assertRaises(HTTPException) as context:
            await self._validate_request(request)

        # Assert the expected error message
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(
            context.exception.detail,
            "Invalid value for 'operation'. Must be 'doMDUpload'.",
        )

    async def test_missing_parameters(self):
        # Create a request with missing required parameters
        request = MagicMock()
        request.headers.get.return_value = "multipart/form-data"
        form_data = FormData(
            {
                "login_id": "user/role",
                "operation": "doMDUpload",
                "mdFile": UploadFile(
                    filename="test.txt", file=self.string_to_binary_io("test")
                ),
            },
        )

        request.form.return_value = self.return_form(form_data)

        # Call the _validate_request method and expect an HTTPException
        with self.assertRaises(HTTPException) as context:
            await self._validate_request(request)

        # Assert the expected error message
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(
            context.exception.detail,
            "Missing required parameters (login_id, login_passwd, "
            "operation).",
        )

    async def test_invalid_content_type(self):
        # Create a request with an invalid content type
        request = MagicMock()
        request.headers.get.return_value = "application/json"
        form_data = FormData(
            {
                "login_id": "user/role",
                "login_passwd": "password",
                "operation": "doMDUpload",
                "mdFile": UploadFile(
                    filename="test.txt", file=self.string_to_binary_io("test")
                ),
            },
        )

        request.form.return_value = self.return_form(form_data)

        # Call the _validate_request method and expect an HTTPException
        with self.assertRaises(HTTPException) as context:
            await self._validate_request(request)

        # Assert the expected error message
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(
            context.exception.detail,
            "Invalid content type. Must be 'multipart/form-data'.",
        )

    async def _validate_request(self, request):
        from opcit.opcit import deposit

        # Call the _validate_request method
        return await deposit.OpCit._validate_request(request)


class TestProcess(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    async def test_process_invalid_xml(self):
        # Mock the _extract_and_validate_request method to return invalid data
        from opcit.opcit.deposit import OpCit

        instance = OpCit(request=Request(scope={"type": "http"}))
        instance._extract_and_validate_request = AsyncMock(
            return_value=(False, None, None, None, None, None)
        )

        # Call the process method
        from starlette.responses import Response as StarletteResponse

        result: StarletteResponse = await instance.process()

        # Assert that the result is as expected
        self.assertIsInstance(result, StarletteResponse)
        self.assertEqual(
            result.body,
            b'<?xml version="1.0" encoding="UTF-8"?><doi_batch_diagnostic '
            b'status="completed" sp="cskAir.local"><record_diagnostic '
            b'status="Failure" msg_id="4"><msg>Record not processed because '
            b"submitted XML does not match any supported schema."
            b' Op Cit only supports 5.3.1"</msg></record_diagnostic>'
            b"<batch_data><record_count>1</record_count><success_count>0"
            b"</success_count><warning_count>0</warning_count>"
            b"<failure_count>1</failure_count></batch_data>"
            b"</doi_batch_diagnostic>",
        )
        self.assertEqual(result.status_code, 400)

    async def test_process_valid_xml(self):
        from opcit.opcit.deposit import OpCit

        instance = OpCit(request=Request(scope={"type": "http"}))
        instance._extract_and_validate_request = AsyncMock(
            return_value=(True, None, None, None, None, None)
        )
        instance._process_dois = AsyncMock(
            return_value={"doi1": MagicMock(), "doi2": MagicMock()}
        )

        # Mock the _extract_fields and deposit methods
        instance._extract_fields = AsyncMock(
            return_value=(None, None, False, [], None, None, None, None)
        )
        instance.deposit = MagicMock()

        # Call the process method
        from starlette.responses import Response as StarletteResponse

        result: StarletteResponse = await instance.process()

        # Assert that the result is as expected

        self.assertIsInstance(result, StarletteResponse)

        # TODO: this will need updating when we decide on the
        #  appropriate response
        self.assertEqual(result.body, b"Welcome to Op Cit")
        self.assertEqual(result.status_code, 200)

        # Assert that the _extract_fields and deposit methods were called
        instance._extract_fields.assert_called()
        self.assertEqual(instance._extract_fields.call_count, 2)
        instance.deposit.assert_not_called()


class TestRewrite(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    async def test_rewrite_journal_article(self):
        # Sample XML content with DOI data elements
        xml_content = """
            <journal_article xmlns="http://www.crossref.org/schema/5.3.1">
                <doi_data>
					<doi>10.32013/123456789-23</doi>
					<resource content_version="vor">https://www.crossref.org/xml-samples/</resource>
					<!-- PDF URL for similarity check -->
					<collection property="crawler-based">
						<item crawler="iParadigms">
							<resource mime_type="application/pdf">https://eprintsds.bbk.ac.uk/id/eprint/26645/1/9780198850489.pdf</resource>
						</item>
					</collection>
					<collection property="text-mining">
						<item>
                            <resource content_version="vor" mime_type="text/xml">https://www.crossref.org/example.xml</resource>
						</item>
					</collection>
				</doi_data>
            </journal_article>
        """
        # load another XML document from 5.3.1.xml using the Pathlib module
        xml_path = Path("../../test_data/5.3.1.xml")

        # Read the XML content from the file
        xml_content_full = etree.fromstring(xml_path.read_bytes())

        # Create an Element object from the XML content
        parsed_xml = etree.fromstring(xml_content)

        date = datetime.datetime.now()

        from opcit.opcit import deposit

        result, md5 = await deposit.OpCit._build_resource(
            doi="10.32013/123456789-23",
            output="https://www.test.com",
            journal_article=parsed_xml,
            title="Journal Title",
            date=date,
            full_tree=xml_content_full,
        )

        self.assertEqual(
            {
                "doi": "10.32013/123456789-23",
                "publication_title": "Journal of Metadata Perfection",
                "title": "Journal Title",
                "resources": [
                    "https://www.test.com",
                    "https://www.crossref.org/xml-samples/",
                ],
                "date": date.isoformat(),
            },
            result,
        )

        self.assertEqual(
            b'<journal_article xmlns="http://www.crossref.org/schema/5.3.1">\n                <doi_data>\n\t\t\t\t\t<doi>10.32013/123456789-23</doi>\n\t\t\t\t\t<resource content_version="vor">https://api.labs.crossref.org/opcit/ed5b0190fc96abbcc0c3c2b97f664b63</resource>\n\t\t\t\t\t<!-- PDF URL for similarity check -->\n\t\t\t\t\t<collection property="crawler-based">\n\t\t\t\t\t\t<item crawler="iParadigms">\n\t\t\t\t\t\t\t<resource mime_type="application/pdf">https://eprintsds.bbk.ac.uk/id/eprint/26645/1/9780198850489.pdf</resource>\n\t\t\t\t\t\t</item>\n\t\t\t\t\t</collection>\n\t\t\t\t\t<collection property="text-mining">\n\t\t\t\t\t\t<item>\n                            <resource content_version="vor" mime_type="text/xml">https://www.crossref.org/example.xml</resource>\n\t\t\t\t\t\t</item>\n\t\t\t\t\t</collection>\n\t\t\t\t</doi_data>\n            </journal_article>',
            etree.tostring(parsed_xml),
        )

    async def test_rewrite_journal_article_from_full(self):
        # load another XML document from 5.3.1.xml using the Pathlib module
        xml_path = Path("../../test_data/5.3.1.xml")

        # Read the XML content from the file
        xml_content_full = etree.fromstring(xml_path.read_bytes())

        # extract the first journal_article
        xml_element = xml_content_full.xpath(
            "//xmlns:journal_article",
            namespaces={"xmlns": f"http://www.crossref.org/schema/5.3.1"},
        )[0]

        date = datetime.datetime.now()

        from opcit.opcit import deposit

        result, md5 = await deposit.OpCit._build_resource(
            doi="10.32013/12345678-23",
            output="https://www.test.com",
            journal_article=xml_element,
            title="Journal Title",
            date=date,
            full_tree=xml_content_full,
        )

        self.assertEqual(
            {
                "doi": "10.32013/12345678-23",
                "publication_title": "Journal of Metadata Perfection",
                "title": "Journal Title",
                "resources": [
                    "https://www.test.com",
                    "https://www.crossref.org/xml-samples/",
                ],
                "date": date.isoformat(),
            },
            result,
        )

        self.assertEqual(
            b'<journal_article xmlns="http://www.crossref.org/schema/5.3.1" xmlns:xsi="htt'
            b'p://www.w3.org/2001/XMLSchema-instance" xmlns:jats="http://www.ncbi.nlm.nih.'
            b'gov/JATS1" xmlns:fr="http://www.crossref.org/fundref.xsd" publication_type="'
            b"full_text\">\n\t\t\t\t<titles>\n\t\t\t\t\t<title>Why 'blah blah blah' is"
            b" the best test data title</title>\n\t\t\t\t</titles>\n\t\t\t\t<contributor"
            b's>\n\t\t\t\t\t<person_name sequence="first" contributor_role="author">'
            b"\n\t\t\t\t\t\t<given_name>Minerva</given_name>\n\t\t\t\t\t\t<surname>da Ho"
            b"usecat</surname>\n\t\t\t\t\t\t<affiliations>\n\t\t\t\t\t\t\t<institutio"
            b'n>\n\t\t\t\t\t\t\t\t<institution_id type="ror">https://ror.org/05gq02987<'
            b"/institution_id>\n\t\t\t\t\t\t\t</institution>\n\t\t\t\t\t\t</affiliations>"
            b'\n\t\t\t\t\t\t<ORCID authenticated="true">https://orcid.org/0000-0002-4011-'
            b"3590</ORCID>\n\t\t\t\t\t</person_name>\n\t\t\t\t</contributors>\n\t\t\t\t<ja"
            b"ts:abstract>\n\t\t\t\t\t<jats:p>Agile\n\t\t\t\t\t\tbest practices, though"
            b"t leadership collective impact impact investing to\n\t\t\t\t\t\tfamilies. A"
            b"nd equal opportunity vibrant, the, storytelling synergy metadata\n\t\t\t"
            b"\t\t\tmatters B-corp unprecedented challenge. Venture philanthropy cultivat"
            b"e\n\t\t\t\t\t\timpact, state of play; white paper collaborative consumption"
            b" entrepreneur\n\t\t\t\t\t\tcollaborative cities inclusive. Parse empower co"
            b"mmunities movements\n\t\t\t\t\t\ttargeted; radical; social enterprise issue"
            b" outcomes big data venture\n\t\t\t\t\t\tphilanthropy. </jats:p>\n\t\t\t\t</j"
            b'ats:abstract>\n\t\t\t\t<publication_date media_type="online">\n\t\t\t\t\t<m'
            b"onth>05</month>\n\t\t\t\t\t<day>01</day>\n\t\t\t\t\t<year>2022</year>\n\t\t"
            b"\t\t</publication_date>\n\t\t\t\t<acceptance_date>\n\t\t\t\t\t<month>05</"
            b"month>\n\t\t\t\t\t<day>21</day>\n\t\t\t\t\t<year>2021</year>\n\t\t\t\t</a"
            b"cceptance_date>\n\t\t\t\t\t\t<!-- CC BY license -->\n\t\t\t\t\t\t<program "
            b'xmlns="http://www.crossref.org/AccessIndicators.xsd">\n\t\t\t\t\t\t\t<free_t'
            b'o_read/>\n\t\t\t\t\t\t\t<license_ref applies_to="tdm" start_date="2022-01-01'
            b'">https://creativecommons.org/licenses/by/4.0/</license_ref>\n\t\t\t\t\t\t\t'
            b'<license_ref applies_to="vor" start_date="2022-01-01">https://creativecommon'
            b"s.org/licenses/by/4.0/</license_ref>\n\t\t\t\t\t\t</program>\n\n\t\t\t\t<"
            b"doi_data>\n\t\t\t\t\t<doi>10.32013/12345678-23</doi>\n\t\t\t\t\t<resource co"
            b'ntent_version="vor">https://api.labs.crossref.org/opcit/ab7348a0f8fd34d56e56'
            b"26dee7b63714</resource>\n\t\t\t\t\t<!-- PDF URL for similarity check -->\n\t"
            b'\t\t\t\t<collection property="crawler-based">\n\t\t\t\t\t\t<item crawler="i'
            b'Paradigms">\n\t\t\t\t\t\t\t<resource mime_type="application/pdf">https://epr'
            b"ints.bbk.ac.uk/id/eprint/26645/1/9780198850489.pdf</resource>\n\t\t\t\t\t\t"
            b'</item>\n\t\t\t\t\t</collection>\n\t\t\t\t\t<collection property="text-minin'
            b'g">\n\t\t\t\t\t\t<item>\n\t\t\t\t\t\t\t<resource content_version="vor" mime'
            b'_type="text/xml">https://www.crossref.org/example.xml</resource>\n\t\t\t'
            b"\t\t\t</item>\n\t\t\t\t\t</collection>\n\t\t\t\t</doi_data>\n\t\t\t</journ"
            b"al_article>\n\n\t\t\t",
            etree.tostring(xml_element),
        )


class TestInterstitialPage(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    async def test_generate_url(self):
        doi = "10.1234/example.doi"
        expected_url = "https://api.labs.crossref.org/opcit/md5_doi"
        expected_md5_doi = "md5_doi"

        import opcit.opcit.deposit

        with patch.object(
            opcit.opcit.deposit.Annotator,
            "doi_to_md5",
            return_value=expected_md5_doi,
        ):
            url, md5_doi = await opcit.opcit.deposit.OpCit._generate_url(doi)
            self.assertEqual(url, expected_url)
            self.assertEqual(md5_doi, expected_md5_doi)


if __name__ == "__main__":
    unittest.main()
