import abc
from typing import Set

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

    @abc.abstractmethod
    def _add(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, user_name: str) -> model.User:
        raise NotImplementedError


class JobRepositoryInterface(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Job]

    def add(self, job: model.Job):
        self._add(job)
        self.seen.add(job)

    def get(self, id_) -> model.Job:
        product = self._get(id_)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, job: model.Job):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id_) -> model.Job:
        raise NotImplementedError
