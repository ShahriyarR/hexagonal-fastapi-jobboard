import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime

from .events import Event, JobCreated, UserCreated


@dataclass
class User:
    uuid: str
    user_name: str
    email: str
    hashed_password: str
    is_active: bool
    is_super_user: bool
    jobs: set["Job"] = field(init=False, default_factory=set)
    events: list[Event] = field(init=False, default_factory=list)

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_)

    def to_dict(self):
        return asdict(self)

    def generate_event(self) -> None:
        user = UserCreated(
            uuid=self.uuid,
            user_name=self.user_name,
            email=self.email,
            hashed_password=self.hashed_password,
            is_super_user=self.is_super_user,
            is_active=self.is_active,
        )
        self.events.append(user)


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


def user_model_event_factory(
    user_name: str,
    email: str,
    hashed_password: str,
    is_active: bool,
    is_super_user: bool,
) -> User:
    user = User(
        uuid=str(uuid.uuid4()),
        user_name=user_name,
        email=email,
        hashed_password=hashed_password,
        is_active=is_active,
        is_super_user=is_super_user,
    )
    user.generate_event()
    return user


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
    events: list[Event] = field(init=False, default_factory=list)

    def generate_event(self) -> None:
        job = JobCreated(
            uuid=self.uuid,
            title=self.title,
            company=self.company,
            company_url=self.company_url,
            location=self.location,
            description=self.description,
            date_posted=self.date_posted,
            is_active=self.is_active,
            owner_id=self.owner_id,
        )
        self.events.append(job)


def job_model_event_factory(
    title: str,
    company: str,
    company_url: str,
    location: str,
    description: str,
    date_posted: str,
    is_active: str,
    owner_id: int,
    owner: User,
) -> Job:
    date_posted_ = date_posted or datetime.now()
    job = Job(
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
    job.generate_event()
    return job


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
