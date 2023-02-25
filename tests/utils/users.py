from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.testclient import TestClient

from src.jobboard.configurator.hashing import Hasher
from src.jobboard.domain.model.model import user_model_factory
from src.jobboard.domain.ports.use_cases.users import UserServiceInterface
from src.jobboard.domain.schemas.users import UserCreateInputDto
from tests.fake_container import Container


@inject
def user_authentication_headers(
    client: TestClient,
    email: str,
    password: str,
):
    data = {"username": email, "password": password}
    r = client.post("/login/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    return {"Authorization": f"Bearer {auth_token}"}


@inject
def authentication_token_from_email(
    client: TestClient,
    email: str,
    user_service: UserServiceInterface = Depends(Provide[Container.fake_user_service]),
):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = "random-passW0rd"
    with user_service.uow:
        user = user_service.uow.users.get_by_email(email=email)
        if not user:
            user_in_create = UserCreateInputDto(
                user_name=email, email=email, password=password
            )
            hashed_password = Hasher.get_password_hash(user_in_create.password)
            new_user = user_model_factory(
                user_name=user_in_create.user_name,
                hashed_password=hashed_password,
                email=user_in_create.email,
                is_active=user_in_create.is_active,
                is_super_user=user_in_create.is_super_user,
            )
            user_service.uow.users.add(new_user)
            user_service.uow.commit()
        return user_authentication_headers(
            client=client, email=email, password=password
        )
