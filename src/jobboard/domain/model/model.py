import uuid
from dataclasses import dataclass, field
from datetime import datetime


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


@dataclass
class Job:
    uuid: str
    title: str
    company: str
    company_url: str
    location: str
    description: str
    date_posted: str
    is_active: str
    owner_id: int
    owner: User


def job_model_factory(
    title: str,
    company: str,
    company_url: str,
    location: str,
    description: str,
    date_posted: str,
    is_active: str,
    owner_id: int,
    owner: User,
):
    date_posted_ = date_posted or datetime.now()
    return Job(
        uuid=str(uuid.uuid4()),
        title=title,
        company=company,
        company_url=company_url,
        location=location,
        description=description,
        date_posted=date_posted_,
        is_active=is_active,
        owner_id=owner_id,
        owner=owner,
    )
