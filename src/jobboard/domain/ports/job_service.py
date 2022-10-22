from typing import Union

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
            job_ = self.uow.jobs.get_by_uuid(new_job.uuid)
            return JobOutputDto.from_orm(job_)

    def retrieve_job(self, id_: int) -> Union[JobOutputDto, bool]:
        with self.uow:
            job = self.uow.jobs.get(id_)
            if not job:
                return False
            job_ = self.uow.jobs.get_by_uuid(job.uuid)
            return JobOutputDto.from_orm(job_)

    def list_jobs(self) -> list[JobOutputDto]:
        with self.uow:
            jobs = self.uow.jobs.get_all()
            return [JobOutputDto.from_orm(job) for job in jobs]

    def update_job_by_id(self, id_: int, job: JobCreateInputDto, owner_id: int) -> bool:
        with self.uow:
            existing_job = self.uow.jobs.get_by_id_for_update(id_)
            if not existing_job:
                return False
            job.__dict__.update(owner_id=owner_id)
            existing_job.owner_id = job.owner_id
            self.uow.commit()
        return True

    def delete_job_by_id(self, id_: int) -> bool:
        with self.uow:
            print("inside")
            existing_job = self.uow.jobs.get(id_)
            print(existing_job)
            if not existing_job:
                print(">>>>")
                return False
            self.uow.session.delete(existing_job)
            self.uow.commit()
        return True

    def search_job(self, query: str) -> list[JobOutputDto]:
        with self.uow:
            return self.uow.jobs.search(query)
