from src.jobboard.domain.model import model
from src.jobboard.domain.ports.repository import (
    JobRepositoryInterface,
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


class JobSqlAlchemyRepository(JobRepositoryInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, job):
        self.session.add(job)

    def _get(self, id_):
        return self.session.query(model.Job).filter_by(id=id_).first()
