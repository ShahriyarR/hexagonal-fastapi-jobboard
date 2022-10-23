from typing import Union

from src.jobboard.domain.model.model import user_model_event_factory
from src.jobboard.domain.ports.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)
from src.jobboard.domain.ports.unit_of_work import UserUnitOfWorkInterface
from src.jobboard.domain.schemas.users import (
    UserCreateInputDto,
    UserLoginInputDto,
    UserOutputDto,
)
from src.jobboard.main.hashing import Hasher


class UserService:
    def __init__(self, uow: UserUnitOfWorkInterface):
        self.uow = uow

    def create(
        self, user: UserCreateInputDto
    ) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            with self.uow:
                user_ = self.uow.users.get(user.user_name)
                if user_ is None:
                    hashed_password = Hasher.get_password_hash(user.password)
                    new_user = user_model_event_factory(
                        user_name=user.user_name,
                        hashed_password=hashed_password,
                        email=user.email,
                        is_active=user.is_active,
                        is_super_user=user.is_super_user,
                    )
                    self.uow.users.add(new_user)
                self.uow.commit()
                user_ = user_ or self.uow.users.get(new_user.user_name)
                user_output_dto = UserOutputDto(
                    user_name=user_.user_name,
                    email=user_.email,
                    is_active=user_.is_active,
                    id=user_.id,
                    is_super_user=user_.is_super_user,
                )
                return ResponseSuccess(user_output_dto)
        except Exception as exc:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

    def authenticate_user(self, user: UserLoginInputDto) -> Union[UserOutputDto, bool]:
        with self.uow:
            user_ = self.uow.users.get_by_email(user.email)
            if not user_ or not Hasher.verify_password(
                user.password, user_.hashed_password
            ):
                return False
            return UserOutputDto(
                id=user_.id,
                user_name=user_.user_name,
                email=user_.email,
                is_active=user_.is_active,
                is_super_user=user_.is_super_user,
            )
