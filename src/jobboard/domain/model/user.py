import uuid
from dataclasses import dataclass, field

from .job import Job


@dataclass
class User:
    uuid: str
    user_name: str
    email: str
    hashed_password: str
    is_active: bool
    is_super_user: bool
    jobs: set[Job] = field(init=False, default_factory=set)


def user_model_factory(
    user_name: str,
    email: str,
    hashed_password: str,
    is_active: bool,
    is_super_user: bool,
) -> User:
    return User(
        uuid=str(uuid.uuid4()),
        user_name=user_name,
        email=email,
        hashed_password=hashed_password,
        is_active=is_active,
        is_super_user=is_super_user,
    )
