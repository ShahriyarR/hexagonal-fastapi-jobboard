import abc
from typing import Union

from src.jobboard.domain.ports.common.responses import ResponseFailure, ResponseSuccess
from src.jobboard.domain.ports.unit_of_work import JobUnitOfWorkInterface
from src.jobboard.domain.schemas.jobs import JobCreateInputDto


class JobServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, uow: JobUnitOfWorkInterface):
        self.uow = uow

    def create(
        self, job: JobCreateInputDto, owner_id: int
    ) -> Union[ResponseFailure, ResponseSuccess]:
        return self._create(job, owner_id)

    def retrieve_job(self, id_: int) -> Union[ResponseFailure, ResponseSuccess]:
        return self._retrieve_job(id_)

    def list_jobs(self) -> ResponseSuccess:
        return self._list_jobs()

    def update_job_by_id(
        self, id_: int, job: JobCreateInputDto, owner_id: int
    ) -> Union[ResponseFailure, ResponseSuccess]:
        return self._update_job_by_id(id_, job, owner_id)

    def delete_job_by_id(self, id_: int) -> Union[ResponseFailure, ResponseSuccess]:
        return self._delete_job_by_id(id_)

    def search_job(self, query: str) -> ResponseSuccess:
        return self._search_job(query)

    @abc.abstractmethod
    def _create(
        self, job: JobCreateInputDto, owner_id: int
    ) -> Union[ResponseFailure, ResponseSuccess]:
        raise NotImplementedError

    @abc.abstractmethod
    def _retrieve_job(self, id_: int) -> Union[ResponseFailure, ResponseSuccess]:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_jobs(self) -> ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_job_by_id(
        self, id_: int, job: JobCreateInputDto, owner_id: int
    ) -> Union[ResponseFailure, ResponseSuccess]:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_job_by_id(self, id_: int) -> Union[ResponseFailure, ResponseSuccess]:
        raise NotImplementedError

    @abc.abstractmethod
    def _search_job(self, query: str) -> ResponseSuccess:
        raise NotImplementedError
