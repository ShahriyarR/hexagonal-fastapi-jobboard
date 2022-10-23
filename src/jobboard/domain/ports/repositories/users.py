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
