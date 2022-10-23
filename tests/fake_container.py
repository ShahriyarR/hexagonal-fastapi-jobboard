from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.jobboard.adapters.db.unit_of_work import (
    JobSqlAlchemyUnitOfWork,
    UserSqlAlchemyUnitOfWork,
)
from src.jobboard.adapters.use_cases.jobs import JobService
from src.jobboard.adapters.use_cases.users import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.jobboard.adapters.entrypoints.webapps.users",
            "src.jobboard.adapters.entrypoints.webapps.auth",
            "src.jobboard.adapters.entrypoints.webapps.jobs",
            "src.jobboard.adapters.entrypoints.api.v1",
            "tests",
        ],
    )

    DEFAULT_SESSION_FACTORY = lambda: sessionmaker(
        bind=create_engine(
            "sqlite:///./test_db.db", connect_args={"check_same_thread": False}
        )
    )

    user_uow = providers.Singleton(
        UserSqlAlchemyUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    job_uow = providers.Singleton(
        JobSqlAlchemyUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )

    fake_user_service = providers.Factory(
        UserService,
        uow=user_uow,
    )

    fake_job_service = providers.Factory(JobService, uow=job_uow)
