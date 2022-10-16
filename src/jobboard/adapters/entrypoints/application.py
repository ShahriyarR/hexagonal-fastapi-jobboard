from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.jobboard.adapters.db.orm import start_mappers
from src.jobboard.adapters.entrypoints.api.base import api_router
from src.jobboard.adapters.entrypoints.webapps.base import api_router as web_app_router
from src.jobboard.main.config import settings
from src.jobboard.main.containers import Container


def configure_static(app):
    app.mount(
        "/static",
        StaticFiles(directory="src/jobboard/adapters/entrypoints/static"),
        name="static",
    )


def include_router(app):
    app.include_router(api_router)
    app.include_router(web_app_router)


def start_application():
    container = Container()
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    app.container = container
    configure_static(app)
    include_router(app)
    start_mappers()
    return app


app = start_application()
