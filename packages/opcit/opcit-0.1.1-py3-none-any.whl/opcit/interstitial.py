import json

from fastapi import Request, Response
from starlette.templating import Jinja2Templates

import settings


class Interstitial:
    def __init__(
        self,
        request: Request,
        instrumentation=None,
    ):
        self.request = request
        self.instrumentation = instrumentation

    async def run(self, identifier) -> Response:
        templates = Jinja2Templates(directory="../templates")

        # load the context from s3
        json_result = json.loads(
            self.instrumentation.aws_connector.s3_obj_to_str(
                bucket=settings.Settings.BUCKET,
                s3_path=f"opcit/works/{identifier}.json",
            )
        )

        json_result["request"] = self.request

        return templates.TemplateResponse(
            "chooser.html",
            json_result,
        )
