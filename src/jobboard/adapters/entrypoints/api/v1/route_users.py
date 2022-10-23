import json

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder

from src.jobboard.adapters.entrypoints import STATUS_CODES
from src.jobboard.hexagon.ports.user_service import UserService
from src.jobboard.hexagon.schemas.users import UserCreateInputDto
from src.jobboard.configurator.containers import Container

router = APIRouter()


@router.post("/")
@inject
def create_user(
    user: UserCreateInputDto,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    response = user_service.create(user=user)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )
