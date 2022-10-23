from src.jobboard.domain.model import model
from src.jobboard.domain.ports.repositories.users import (
    UserRepositoryInterface,
)


class UserSqlAlchemyRepository(UserRepositoryInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, user):
        self.session.add(user)

    def _get(self, user_name: str):
        return self.session.query(model.User).filter_by(user_name=user_name).first()

    def _get_by_email(self, email: str) -> model.User:
        return self.session.query(model.User).filter_by(email=email).first()

    def _get_by_id(self, id: int) -> model.User:
        return self.session.query(model.User).filter_by(id=id).first()