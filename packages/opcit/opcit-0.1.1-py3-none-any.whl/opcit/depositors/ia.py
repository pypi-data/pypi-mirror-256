import io
import time

import clannotation.annotator

import magic
import settings
from internetarchive import get_session, ArchiveSession, exceptions


class Archive:
    def __init__(self, log_function):
        self.log_function = log_function
        self.archive_name = "Internet Archive"

    def deposit(
        self,
        file_object: bytes,
        warnings: list,
        doi: str,
        metadata: dict = None,
    ) -> (list, str):
        """
        Deposit a file to the archive
        :param metadata:
        :param doi: the DOIs
        :param warnings: the warnings dictionary
        :param file_object: the file objects to deposit
        :return: None
        """
        self.log_function(f"Invoking {self.archive_name} depositor")

        mime_proceed, mime_type = self._check_mimes(file_object, warnings, doi)

        if not mime_proceed:
            return warnings

        ia_session = self._get_ia_session()

        remote_file = clannotation.annotator.Annotator.doi_to_md5(doi)
        ia_item = ia_session.get_item(remote_file)

        # if metadata's date field is datetime, convert to string
        if metadata.get("date"):
            metadata["date"] = str(metadata["date"])

        r = ia_item.upload(
            files={
                str(time.time())
                + "-"
                + remote_file
                + ".pdf": io.BytesIO(file_object)
            },
            metadata=metadata,
        )

        try:
            ia_item.modify_metadata(metadata)
        except exceptions.ItemLocateError:
            message = (
                f"Failed to modify metadata for {remote_file} "
                f"in {self.archive_name} for {doi}."
            )
            warnings.append(message)
            self.log_function(message)

        return warnings, ia_item.urls.details

    def _check_mimes(
        self, file_object: bytes, warnings: list, doi: str
    ) -> tuple[bool, list]:
        """
        Check the MIME type of the file
        :param file_object: the file object to check
        :param warnings: the warnings list
        :param doi: the DOI
        :return: tuple of bool for success and list of warnings
        """
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(file_object)

        self.log_function(f"File MIME type for {doi} is {mime_type}")

        if mime_type != "application/pdf":
            message = (
                f"File MIME type for {doi} is {mime_type}. "
                "This item will not be archived as only PDF is supported."
            )
            warnings.append(message)
            self.log_function(message)

            return False, warnings
        else:
            return True, warnings

    @staticmethod
    def _get_ia_session() -> ArchiveSession:
        """
        Get an Internet Archive session, fetching secrets from AWS
        :return: the session
        """
        settings.Settings.fetch_secrets()

        config = {
            "s3": {
                "access": settings.Settings.ACCESS_KEY["access_key"],
                "secret": settings.Settings.ACCESS_KEY["secret_key"],
            }
        }
        ia_session = get_session(config=config)
        return ia_session
