import contextlib

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator

from src.jobboard.adapters.db.orm import start_mappers
from src.jobboard.adapters.entrypoints.api.base import api_router
from src.jobboard.adapters.entrypoints.webapps.base import api_router as web_app_router
from src.jobboard.configurator.config import settings
from src.jobboard.configurator.containers import Container
from src.jobboard.configurator.tracer.jaeger_tracing import tracer


def configure_static(app):
    app.mount(
        "/static",
        StaticFiles(directory="src/jobboard/adapters/entrypoints/static"),
        name="static",
    )


def include_router(app_):
    app_.include_router(api_router)
    app_.include_router(web_app_router)


def _configure_logger(app_):
    app_.logger = Container.LOGGER


def _configure_tracer(app_):
    FastAPIInstrumentor.instrument_app(app_, tracer_provider=tracer)


def start_application():
    container = Container()
    app_ = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app_.container = container
    _configure_logger(app_)
    _configure_tracer(app_)
    configure_static(app_)
    include_router(app_)
    start_mappers()
    return app_


app = start_application()


@app.on_event("startup")
async def startup():
    with contextlib.suppress(ValueError):
        Instrumentator().instrument(app).expose(app)
