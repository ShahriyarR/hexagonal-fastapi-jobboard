from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.jobboard.adapters.db.orm import start_mappers
from src.jobboard.adapters.entrypoints.api.base import api_router
from src.jobboard.adapters.entrypoints.webapps.base import api_router as web_app_router
from src.jobboard.configurator.config import settings
from src.jobboard.configurator.containers import Container
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from src.jobboard.configurator.tracer.jaeger_tracing import tracer


def configure_static(app):
    app.mount(
        "/static",
        StaticFiles(directory="src/jobboard/adapters/entrypoints/static"),
        name="static",
    )


def include_router(app):
    app.include_router(api_router)
    app.include_router(web_app_router)


def _configure_logger(app):
    app.logger = Container.LOGGER


def _configure_tracer(app):
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)


def start_application():
    container = Container()
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.container = container
    _configure_logger(app)
    _configure_tracer(app)
    configure_static(app)
    include_router(app)
    start_mappers()
    return app


app = start_application()
