from typing import Union

from src.jobboard.domain.model.model import job_model_event_factory
from src.jobboard.domain.ports.common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)
from src.jobboard.domain.ports.unit_of_works.jobs import JobUnitOfWorkInterface
from src.jobboard.domain.ports.use_cases.jobs import JobServiceInterface
from src.jobboard.domain.schemas.jobs import JobCreateInputDto, JobOutputDto


def _handle_response_failure(
    id_: int = None, message: dict[str] = None
) -> ResponseFailure:
    return (
        ResponseFailure(
            ResponseTypes.RESOURCE_ERROR,
            message=message,
        )
        if message
        else ResponseFailure(
            ResponseTypes.RESOURCE_ERROR,
            message={"detail": f"Job with id {id_} not found"},
        )
    )


class JobService(JobServiceInterface):
    def __init__(self, uow: JobUnitOfWorkInterface):
        self.uow = uow

    def _create(
        self, job: JobCreateInputDto, owner_id: int
    ) -> Union[ResponseFailure, ResponseSuccess]:
        try:
            with self.uow:
                new_job = job_model_event_factory(**job.dict(), owner_id=owner_id)
                self.uow.jobs.add(new_job)
                self.uow.commit()
                job_ = self.uow.jobs.get_by_uuid(new_job.uuid)
                return (
                    ResponseSuccess(JobOutputDto.from_orm(job_))
                    if job_
                    else _handle_response_failure(
                        message={"detail": "Could not find newly created job"}
                    )
                )

        except Exception as exc:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

    def _retrieve_job(self, id_: int) -> Union[ResponseFailure, ResponseSuccess]:
        with self.uow:
            job = self.uow.jobs.get(id_)
            return (
                ResponseSuccess(JobOutputDto.from_orm(job))
                if job
                else _handle_response_failure(id_)
            )

    def _list_jobs(self) -> ResponseSuccess:
        with self.uow:
            jobs = self.uow.jobs.get_all()
            return ResponseSuccess([JobOutputDto.from_orm(job) for job in jobs])

    def _update_job_by_id(
        self, id_: int, job: JobCreateInputDto, owner_id: int
    ) -> Union[ResponseFailure, ResponseSuccess]:
        with self.uow:
            existing_job = self.uow.jobs.get_by_id_for_update(id_)
            if not existing_job:
                return _handle_response_failure(id_)
            job.__dict__.update(owner_id=owner_id)
            existing_job.owner_id = job.owner_id
            self.uow.commit()
            job_ = self.uow.jobs.get(id_)
            return ResponseSuccess(JobOutputDto.from_orm(job_))

    def _delete_job_by_id(self, id_: int) -> Union[ResponseFailure, ResponseSuccess]:
        with self.uow:
            existing_job = self.uow.jobs.get(id_)
            if not existing_job:
                return _handle_response_failure(id_)
            self.uow.session.delete(existing_job)
            self.uow.commit()
            return ResponseSuccess(value={"detail": "Successfully deleted."})

    def _search_job(self, query: str) -> ResponseSuccess:
        with self.uow:
            result = self.uow.jobs.search(query)
            return ResponseSuccess(value=result)
