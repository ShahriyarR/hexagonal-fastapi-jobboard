from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from src.jobboard.adapters.db import repository
from src.jobboard.domain.ports.unit_of_work import (
    JobUnitOfWorkInterface,
    UserUnitOfWorkInterface,
)
from src.jobboard.main import config

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_database_uri(), connect_args={"check_same_thread": False}
    )
)


class UserSqlAlchemyUnitOfWork(UserUnitOfWorkInterface):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.users = repository.UserSqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class JobSqlAlchemyUnitOfWork(JobUnitOfWorkInterface):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.jobs = repository.JobSqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
