from dependency_injector import containers, providers

from src.jobboard.adapters.db.unit_of_work import UserSqlAlchemyUnitOfWork
from src.jobboard.domain.ports.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.jobboard.adapters.entrypoints.webapps.users",
            "src.jobboard.adapters.entrypoints.webapps.auth",
            "src.jobboard.adapters.entrypoints.api.v1",
        ]
    )

    uow = providers.Singleton(UserSqlAlchemyUnitOfWork)

    user_service = providers.Factory(
        UserService,
        uow=uow,
    )
