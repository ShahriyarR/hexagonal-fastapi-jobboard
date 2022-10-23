from typing import Any, Callable

from sqlalchemy.orm.session import Session

from src.jobboard.adapters.repositories.jobs import JobSqlAlchemyRepository
from src.jobboard.domain.ports.unit_of_works.jobs import JobUnitOfWorkInterface


class JobSqlAlchemyUnitOfWork(JobUnitOfWorkInterface):
    def __init__(self, session_factory: Callable[[], Any]):
        self.session_factory = session_factory()

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.jobs = JobSqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
