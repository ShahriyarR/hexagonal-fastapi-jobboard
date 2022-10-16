from typing import Union

from src.jobboard.domain.model.model import user_model_event_factory
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

    def create(self, user: UserCreateInputDto) -> UserOutputDto:
        with self.uow:
            user_ = self.uow.users.get(user.user_name)
            if user_ is None:
                hashed_password = Hasher.get_password_hash(user.password)
                new_user = user_model_event_factory(
                    user_name=user.user_name,
                    hashed_password=hashed_password,
                    email=user.email,
                    is_active=True,
                    is_super_user=False,
                )
                self.uow.users.add(new_user)
            self.uow.commit()
            return UserOutputDto(
                user_name=user_.user_name, email=user_.email, is_active=user_.is_active
            )

    def authenticate_user(self, user: UserLoginInputDto) -> Union[UserOutputDto, bool]:
        with self.uow:
            user_ = self.uow.users.get_by_email(user.email)
            if not user_:
                return False
            if not Hasher.verify_password(user.password, user_.hashed_password):
                return False
            return UserOutputDto(
                user_name=user_.user_name, email=user_.email, is_active=user_.is_active
            )
