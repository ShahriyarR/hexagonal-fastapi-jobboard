import uuid
from dataclasses import dataclass
from datetime import datetime

from .user import User


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
