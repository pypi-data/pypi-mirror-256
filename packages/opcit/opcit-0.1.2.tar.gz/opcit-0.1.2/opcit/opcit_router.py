try:
    import settings
    import deposit as deposit_system
except ImportError:
    import opcit.settings as settings
    import opcit.deposit as deposit_system

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from longsight.instrumentation import instrument


router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.post("/deposit/preserve/", tags=["deposit", "preservation"])
@instrument(
    create_aws=True,
    bucket=settings.Settings.BUCKET,
    sign_aws_requests=True,
    cloudwatch_push=True,
    log_group_name=settings.Settings.LOG_STREAM_GROUP,
    log_stream_name=settings.Settings.LOG_STREAM_NAME,
)
async def deposit(
    request: Request,
    instrumentation=None,
):
    return await deposit_system.OpCit(
        request=request, instrumentation=instrumentation
    ).process()


@router.get("/opcit/{identifier}/", tags=["preservation"])
@instrument(
    create_aws=True,
    bucket=settings.Settings.BUCKET,
    sign_aws_requests=True,
    cloudwatch_push=True,
    log_group_name=settings.Settings.LOG_STREAM_GROUP,
    log_stream_name=settings.Settings.LOG_STREAM_NAME,
)
async def deposit(
    request: Request,
    instrumentation=None,
    identifier: str = None,
):
    import opcit.opcit.interstitial

    return await opcit.opcit.interstitial.Interstitial(
        request=request, instrumentation=instrumentation
    ).run(identifier)
