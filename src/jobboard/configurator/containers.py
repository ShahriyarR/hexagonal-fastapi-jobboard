from pathlib import Path

from dependency_injector import containers, providers
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.jobboard.adapters.unit_of_works.jobs import JobSqlAlchemyUnitOfWork
from src.jobboard.adapters.unit_of_works.users import UserSqlAlchemyUnitOfWork
from src.jobboard.adapters.use_cases.jobs import JobService
from src.jobboard.adapters.use_cases.users import UserService
from src.jobboard.configurator import config
from src.jobboard.configurator.logger.custom_logging import CustomizeLogger

ENGINE = create_engine(
    config.get_database_uri(), connect_args={"check_same_thread": False}
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.jobboard.adapters.entrypoints.webapps.users",
            "src.jobboard.adapters.entrypoints.webapps.auth",
            "src.jobboard.adapters.entrypoints.webapps.jobs",
            "src.jobboard.adapters.entrypoints.api.v1",
        ]
    )

    config_path = Path(__file__).parent / "logger/logging_config.json"
    LOGGER = CustomizeLogger.make_logger(config_path)
    SQLAlchemyInstrumentor().instrument(
        engine=ENGINE, enable_commenter=True, commenter_options={}
    )
    DEFAULT_SESSION_FACTORY = lambda: sessionmaker(bind=ENGINE)

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

    job_service = providers.Factory(JobService, uow=job_uow)
