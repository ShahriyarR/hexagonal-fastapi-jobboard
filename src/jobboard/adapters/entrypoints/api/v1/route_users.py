from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.jobboard.domain.ports.user_service import UserService
from src.jobboard.domain.schemas.users import UserCreateInputDto, UserOutputDto
from src.jobboard.main.containers import Container

router = APIRouter()


@router.post("/", response_model=UserOutputDto)
@inject
def create_user(
    user: UserCreateInputDto,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    print(user)
    print(user_service.uow)
    user = user_service.create(user=user)
    return user
