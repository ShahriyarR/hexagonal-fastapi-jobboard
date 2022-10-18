from fastapi.testclient import TestClient

from src.jobboard.domain.schemas.users import UserCreateInputDto


def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("/login/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(client: TestClient, email: str):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    password = "random-passW0rd"
    user = get_user_by_email(
        email=email,
    )
    if not user:
        user_in_create = UserCreateInputDto(
            username=email, email=email, password=password
        )
        user = create_new_user(user=user_in_create)
    return user_authentication_headers(client=client, email=email, password=password)
