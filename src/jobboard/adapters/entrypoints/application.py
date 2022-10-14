from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.jobboard.adapters.db.orm import start_mappers
from src.jobboard.main.config import settings


def configure_static(app):
    app.mount(
        "/static",
        StaticFiles(directory="src/jobboard/adapters/entrypoints/static"),
        name="static",
    )


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    configure_static(app)
    start_mappers()
    return app


app = start_application()
