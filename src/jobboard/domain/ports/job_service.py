from src.jobboard.domain.model.model import job_model_event_factory
from src.jobboard.domain.ports.unit_of_work import JobUnitOfWorkInterface
from src.jobboard.domain.schemas.jobs import JobCreateInputDto, JobOutputDto


class JobService:
    def __init__(self, uow: JobUnitOfWorkInterface):
        self.uow = uow

    def create(self, job: JobCreateInputDto, owner_id: int) -> JobOutputDto:
        with self.uow:
            new_job = job_model_event_factory(**job.dict(), owner_id=owner_id)
            self.uow.jobs.add(new_job)
            self.uow.commit()
            return JobOutputDto(**new_job.to_dict())

    def retrieve_job(self, id_: int) -> JobOutputDto:
        ...

    def list_jobs(self) -> list[JobOutputDto]:
        ...

    def update_job_by_id(self, id_: int, job: JobCreateInputDto) -> bool:
        ...

    def delete_job_by_id(self, id_: int) -> bool:
        ...

    def search_job(self, query: str) -> list[JobOutputDto]:
        ...
