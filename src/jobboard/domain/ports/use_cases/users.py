import abc
from typing import Union

from src.jobboard.domain.ports.common.responses import ResponseFailure, ResponseSuccess
from src.jobboard.domain.ports.unit_of_work import UserUnitOfWorkInterface
from src.jobboard.domain.schemas.users import (
    UserCreateInputDto,
    UserLoginInputDto,
    UserOutputDto,
)


class UsersServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: UserUnitOfWorkInterface):
        self.uow = uow

    def create(
        self, user: UserCreateInputDto
    ) -> Union[ResponseSuccess, ResponseFailure]:
        return self._create(user)

    def authenticate_user(self, user: UserLoginInputDto) -> Union[UserOutputDto, bool]:
        return self._authenticate_user(user)

    @abc.abstractmethod
    def _create(
        self, user: UserCreateInputDto
    ) -> Union[ResponseSuccess, ResponseFailure]:
        raise NotImplementedError

    @abc.abstractmethod
    def _authenticate_user(self, user: UserLoginInputDto) -> Union[UserOutputDto, bool]:
        raise NotImplementedError
