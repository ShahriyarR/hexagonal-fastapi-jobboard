from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.jobboard.adapters.db.unit_of_work import (
    JobSqlAlchemyUnitOfWork,
    UserSqlAlchemyUnitOfWork,
)
from src.jobboard.adapters.use_cases.jobs import JobsService
from src.jobboard.domain.ports.user_service import UserService
from src.jobboard.configurator import config


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.jobboard.adapters.entrypoints.webapps.users",
            "src.jobboard.adapters.entrypoints.webapps.auth",
            "src.jobboard.adapters.entrypoints.webapps.jobs",
            "src.jobboard.adapters.entrypoints.api.v1",
        ]
    )

    DEFAULT_SESSION_FACTORY = lambda: sessionmaker(
        bind=create_engine(
            config.get_database_uri(), connect_args={"check_same_thread": False}
        )
    )

    user_uow = providers.Singleton(
        UserSqlAlchemyUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    job_uow = providers.Singleton(
        JobSqlAlchemyUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )

    user_service = providers.Factory(
        UserService,
        uow=user_uow,
    )

    job_service = providers.Factory(JobsService, uow=job_uow)
