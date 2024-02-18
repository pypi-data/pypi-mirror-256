import hashlib
import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch, Mock


class TestDeposit(unittest.TestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    def log(self, message):
        return

    @patch("opcit.opcit.depositors.ia.time")
    def test_deposit_success(self, mock_time):
        """
        Test the deposit method with a successful deposit
        """
        # Mock the _check_mimes and _get_ia_session methods
        mock_check_mimes = Mock(return_value=(True, "application/pdf"))
        mock_get_ia_session = Mock()

        from opcit.opcit.depositors.ia import Archive

        instance = Archive(self.log)
        instance._check_mimes = mock_check_mimes
        instance._get_ia_session = mock_get_ia_session

        # Mock the return values for IAItem and its methods
        mock_ia_item = Mock()
        mock_ia_item.upload.return_value = Mock()
        mock_ia_item.urls.details = "https://example.com/item_details"

        mock_get_ia_session.return_value.get_item.return_value = mock_ia_item

        # Set the metadata and file object
        metadata = {"date": "2022-01-01"}
        file_object = b"File content"

        # Call the deposit method
        warnings, details_url = instance.deposit(
            file_object, [], "example_doi", metadata
        )

        # Assert that the mocks were called correctly
        mock_check_mimes.assert_called_once_with(file_object, [], "example_doi")
        mock_get_ia_session.assert_called_once()
        mock_time.time.assert_called_once()

        mock_ia_item.upload.assert_called_once_with(
            files={
                "{}-{}.pdf".format(
                    mock_time.time(),
                    hashlib.md5("example_doi".encode()).hexdigest(),
                ): mock.ANY
            },
            metadata=metadata,
        )
        mock_ia_item.modify_metadata.assert_called_once_with(metadata)

        self.assertEqual(warnings, [])
        self.assertEqual(details_url, "https://example.com/item_details")

    def test_deposit_mime_failure(self):
        """
        Test the deposit method with a MIME type failure
        """
        # Mock the _check_mimes method to return False
        mock_check_mimes = Mock(return_value=(False, "invalid/mime_type"))

        # Set up the mock instance of YourClass
        from opcit.opcit.depositors.ia import Archive

        instance = Archive(self.log)
        instance._check_mimes = mock_check_mimes

        # Call the deposit method
        warnings = instance.deposit(b"File content", [], "example_doi")

        # Assert that the mock was called correctly
        mock_check_mimes.assert_called_once_with(
            b"File content", [], "example_doi"
        )

        self.assertEqual(warnings, [])


class TestCheckMimes(unittest.TestCase):
    def setUp(self):
        # Create a mock object for the logger
        self.logger = MagicMock()
        sys.path.append("../opcit/")

    def test_valid_pdf(self):
        """
        Test the _check_mimes function with a valid PDF file
        """
        # Simulate a valid PDF file by setting mime_type to "application/pdf"
        mime_type = "application/pdf"
        warnings = []

        # Call the _check_mimes function with the mock logger
        result, new_warnings = self._check_mimes(mime_type, warnings, "doi")

        # Assert that the function returns True for a valid PDF
        self.assertTrue(result)

        # Assert that the warnings list is unchanged
        self.assertEqual(new_warnings, [])

        # Assert that the logger was called with the correct message
        self.logger.assert_called_once_with(
            "File MIME type for doi is application/pdf"
        )

    def test_invalid_mime_type(self):
        """
        Test the _check_mimes function with an invalid MIME type
        """
        # Simulate an invalid MIME type
        mime_type = "image/jpeg"
        warnings = []

        # Call the _check_mimes function with the mock logger
        result, new_warnings = self._check_mimes(mime_type, warnings, "doi")

        # Assert that the function returns False for an invalid MIME type
        self.assertFalse(result)

        # Assert that the warnings list contains the expected warning message
        self.assertEqual(len(new_warnings), 1)
        expected_warning = (
            "File MIME type for doi is image/jpeg. This item will "
            "not be archived as only PDF is supported."
        )
        self.assertEqual(new_warnings[0], expected_warning)

    def _check_mimes(self, mime_type, warnings, doi):
        """
        Helper function to call the _check_mimes function with a mock logger
        :param mime_type: the MIME type to return from the mock
        :param warnings: the warnings list to pass to the function
        :param doi: the DOI to pass to the function
        :return: the result and new_warnings from the function
        """
        # Mock the 'magic' library's Magic class and its 'from_buffer' method
        from unittest.mock import patch

        with patch("magic.Magic") as mock_magic:
            mock_instance = mock_magic.return_value
            mock_instance.from_buffer.return_value = mime_type

            # Call the _check_mimes function with the mock logger
            from opcit.opcit.depositors import ia

            instance = ia.Archive(self.logger)
            result, new_warnings = instance._check_mimes(b"", warnings, doi)

        return result, new_warnings


class TestGetIaSession(unittest.TestCase):
    @patch("opcit.opcit.settings.Settings")
    @patch("opcit.opcit.depositors.ia.get_session")
    @patch("opcit.opcit.settings.json.loads")
    @patch("opcit.opcit.settings.claws.aws_utils.AWSConnector")
    def test_get_ia_session(
        self,
        mock_aws_connector,
        mock_json_loads,
        mock_get_session,
        mock_settings,
    ):
        """
        Test the _get_ia_session function
        """
        # Mock the settings.Settings.fetch_secrets method
        mock_settings.fetch_secrets.return_value = None

        # Mock the get_session method
        from internetarchive import ArchiveSession

        mock_session = MagicMock(spec=ArchiveSession)
        mock_get_session.return_value = mock_session

        # mock the settings access key function
        # Set up the mocks for the AWSConnector and json.loads methods
        mock_secret = (
            '{"access_key": "test_access_key", "secret_key": "test_secret_key"}'
        )
        mock_aws_connector.return_value.get_secret.return_value = mock_secret
        mock_json_loads.return_value = {
            "access_key": "test_access_key",
            "secret_key": "test_secret_key",
        }

        # Call the _get_ia_session function
        from opcit.opcit.depositors.ia import Archive

        result = Archive._get_ia_session()

        # Assert that the methods were called correctly

        mock_get_session.assert_called_once_with(
            config={
                "s3": {
                    "access": "test_access_key",
                    "secret": "test_secret_key",
                }
            }
        )
        self.assertEqual(result, mock_session)


if __name__ == "__main__":
    unittest.main()
