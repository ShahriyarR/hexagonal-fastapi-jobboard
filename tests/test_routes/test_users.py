from fastapi.encoders import jsonable_encoder

from src.jobboard.domain.schemas.users import UserCreateInputDto


def test_create_user(app, client, get_fake_container):
    data = {
        "user_name": "testuser",
        "email": "testuser@nofoobar.com",
        "password": "testing",
    }
    data = UserCreateInputDto(**data)
    with app.container.user_service.override(get_fake_container.fake_user_service):
        response = client.post("/users/", json=jsonable_encoder(data))
        assert response.status_code == 200
        assert response.json()["email"] == "testuser@nofoobar.com"
        assert response.json()["is_active"] == True
