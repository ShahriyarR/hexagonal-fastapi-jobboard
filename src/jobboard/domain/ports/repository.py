import abc
from typing import Set

from sqlalchemy.orm import Query

from src.jobboard.domain.model import model


class UserRepositoryInterface(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.User]

    def add(self, user: model.User):
        self._add(user)
        self.seen.add(user)

    def get(self, user_name: str) -> model.User:
        user = self._get(user_name)
        if user:
            self.seen.add(user)
        return user

    def get_by_email(self, email: str) -> model.User:
        user = self._get_by_email(email)
        if user:
            self.seen.add(user)
        return user

    def get_by_id(self, id: int) -> model.User:
        user = self._get_by_id(id)
        if user:
            self.seen.add(user)
        return user

    @abc.abstractmethod
    def _add(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, user_name: str) -> model.User:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_email(self, email: str) -> model.User:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id(self, id: int) -> model.User:
        raise NotImplementedError


class JobRepositoryInterface(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Job]

    def add(self, job: model.Job):
        self._add(job)
        self.seen.add(job)

    def get(self, id_) -> model.Job:
        job = self._get(id_)
        if job:
            self.seen.add(job)
        return job

    def get_by_uuid(self, uuid: str) -> model.Job:
        job = self._get_by_uuid(uuid)
        if job:
            self.seen.add(job)
        return job

    def get_by_id_for_update(self, id_: int) -> Query:
        job = self._get_by_id_for_update(id_)
        if job and job.first():
            self.seen.add(job.first())
        return job

    def get_all(self) -> list[model.Job]:
        return self._get_all()

    def search(self, query: str):
        return self._search(query)

    @abc.abstractmethod
    def _add(self, job: model.Job):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id_: int) -> model.Job:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_uuid(self, uuid: str) -> model.Job:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(self) -> list[model.Job]:
        raise NotImplementedError

    @abc.abstractmethod
    def _search(self, query: str) -> list[model.Job]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_id_for_update(self, id_: int):
        raise NotImplementedError
