from dependency_injector import containers, providers

from src.jobboard.adapters.db.unit_of_work import (
    JobSqlAlchemyUnitOfWork,
    UserSqlAlchemyUnitOfWork,
)
from src.jobboard.domain.ports.job_service import JobService
from src.jobboard.domain.ports.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.jobboard.adapters.entrypoints.webapps.users",
            "src.jobboard.adapters.entrypoints.webapps.auth",
            "src.jobboard.adapters.entrypoints.api.v1",
        ]
    )

    user_uow = providers.Singleton(UserSqlAlchemyUnitOfWork)
    job_uow = providers.Singleton(JobSqlAlchemyUnitOfWork)

    user_service = providers.Factory(
        UserService,
        uow=user_uow,
    )

    job_service = providers.Factory(JobService, uow=job_uow)
