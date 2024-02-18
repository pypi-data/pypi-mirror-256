import json
from collections import OrderedDict

import claws.aws_utils


class Settings:
    BUCKET = "outputs.research.crossref.org"
    SAMPLES_BUCKET = "samples.research.crossref.org"

    APP_NAME = "Op Cit Deposit System"
    ABOUT = "A digital preservation deposit system for Crossref's Labs API"
    VERSION = "0.0.1"
    MAILTO = "labs@crossref.org"
    LICENSE_INFO = {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
    TERMS_OF_SERVICE = """
        Warnings, Caveats and Weasel Words:

        This is an experiment running on R&D equipment in a non-production environment.

        It may disappear without warning and/or perform erratically.

        If it isn’t working for some reason, come back later and try again.
    """

    SCHEME = "https"
    REPRESENTATION_VERSION = "1.0.0"

    HEADERS = {"User-Agent": "f{APP_NAME}; mailto:{MAILTO}"}

    LOG_STREAM_NAME = "op-cit-deposit"
    LOG_STREAM_GROUP = "op-cit"

    DEPOSIT_SYSTEMS = {"Internet Archive": "ia"}

    AWS_CONNECTOR = None
    ACCESS_KEY = {}

    @staticmethod
    def fetch_secrets():
        if Settings.ACCESS_KEY == {}:
            Settings.AWS_CONNECTOR = claws.aws_utils.AWSConnector(
                unsigned=False, bucket=Settings.BUCKET, region_name="us-east-1"
            )

            Settings.ACCESS_KEY = json.loads(
                Settings.AWS_CONNECTOR.get_secret("InternetArchiveS3LikeAPI")
            )
