from sqlalchemy import Boolean, Column, Date, Integer, MetaData, String, Table, event
from sqlalchemy.orm import registry, relationship

from src.jobboard.domain.model import model

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

jobs = Table(
    "jobs",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("company", String, nullable=False),
    Column("company_url", String),
    Column("location", String, nullable=False),
    Column("description", String, nullable=False),
    Column("date_posted", Date),
    Column("is_active", Boolean(), default=True),
)

users = Table(
    "users",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_name", String, unique=True, nullable=False),
    Column("email", String, nullable=False, unique=True, index=True),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean(), default=True),
    Column("is_superuser", Boolean(), default=False),
)


def start_mappers():
    jobs_mapper = mapper_registry.map_imperatively(model.Job, jobs)
    mapper_registry.map_imperatively(
        model.User, users, properties={"jobs": relationship(jobs_mapper)}
    )


@event.listens_for(model.Job, "load")
def receive_load(job, _):
    job.events = []


@event.listens_for(model.User, "load")
def receive_load(user, _):
    user.events = []