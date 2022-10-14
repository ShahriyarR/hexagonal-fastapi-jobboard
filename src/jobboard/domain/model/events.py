from dataclasses import asdict, dataclass, field

from .model import Job, User


class Event:
    pass


@dataclass
class UserCreated(Event):
    uuid: str
    user_name: str
    email: str
    hashed_password: str
    is_active: bool
    is_super_user: bool
    jobs: set[Job] = field(init=False, default_factory=set)

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_)

    def to_dict(self):
        return asdict(self)


@dataclass
class JobCreated(Event):
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

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_)

    def to_dict(self):
        return asdict(self)
