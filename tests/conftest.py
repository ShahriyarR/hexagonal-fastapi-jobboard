import uuid
from datetime import datetime
from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.jobboard.adapters.db.orm import metadata
from src.jobboard.adapters.entrypoints.application import app as original_app
from src.jobboard.main.config import settings
from tests.fake_container import Container
from tests.utils.users import authentication_token_from_email

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module", autouse=True)
def get_fake_container():
    return Container()


@pytest.fixture(scope="module")
def app(get_fake_container):
    metadata.create_all(engine)
    yield original_app
    metadata.drop_all(engine)


@pytest.fixture
def get_user_model_dict():
    return {
        "uuid": str(uuid.uuid4()),
        "user_name": "shako",
        "email": "rzayev.sehriyar@gmail.com",
        "hashed_password": "password",
        "is_active": True,
        "is_super_user": False,
    }


@pytest.fixture
def get_job_model_dict():
    return {
        "uuid": str(uuid.uuid4()),
        "title": "Awesome Title",
        "company": "Awesome LLC",
        "company_url": "http://awesome.com",
        "location": "Azerbaijan",
        "description": "It is a trap!",
        "date_posted": datetime.now(),
        "is_active": True,
        "owner_id": 1,
    }


@pytest.fixture(scope="module")
def client(
    app: FastAPI,
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def normal_user_token_headers(
    client: TestClient,
    get_fake_container,
    app,
):
    with app.container.user_service.override(get_fake_container.fake_user_service):
        return authentication_token_from_email(
            client=client,
            email=settings.TEST_USER_EMAIL,
        )
