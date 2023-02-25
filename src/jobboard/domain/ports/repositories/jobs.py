import abc

from src.jobboard.domain.model import model


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

    def get_by_id_for_update(self, id_: int) -> model.Job:
        job = self._get_by_id_for_update(id_).first()
        if job:
            self.seen.add(job)
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
