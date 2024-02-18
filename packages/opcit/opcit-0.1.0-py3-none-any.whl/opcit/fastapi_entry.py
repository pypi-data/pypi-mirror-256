import pathlib
import sys

path = pathlib.Path("/app/app")

if path.exists():
    sys.path.append("/app/app")
    sys.path.append("/app/app/templates")

import longsight.instrumentation as instrumentation
from fastapi import FastAPI
from opcit.opcit import opcit_router

app = FastAPI(
    description="A test API to demonstrate Op Cit",
    title="Op Cit Test",
    version="0.0.1",
    contact={"email": "meve@crossref.org"},
    license_info={},
    terms_of_service="Terms",
)

app.router.route_class = instrumentation.LoggerRouteHandler

# note that the annotation router should be last, as it is the fallback route
app.include_router(opcit_router.router)


app.add_middleware(instrumentation.AWSCorrelationIdMiddleware)
