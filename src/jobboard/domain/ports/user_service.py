from src.jobboard.domain.model.model import user_model_event_factory
from src.jobboard.domain.ports.unit_of_work import UserUnitOfWorkInterface
from src.jobboard.domain.schemas.users import UserInputDto
from src.jobboard.main.hashing import Hasher


class UserService:
    def __init__(self, uow: UserUnitOfWorkInterface):
        self.uow = uow

    def create(self, user: UserInputDto):
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
