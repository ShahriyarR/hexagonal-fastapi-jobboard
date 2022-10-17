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
        with self.uow:
            job = self.uow.jobs.get(id_)
            return JobOutputDto(**job.to_dict())

    def list_jobs(self) -> list[JobOutputDto]:
        with self.uow:
            jobs = self.uow.jobs.get_all()
            return [JobOutputDto(**job.to_dict()) for job in jobs]

    def update_job_by_id(self, id_: int, job: JobCreateInputDto, owner_id: int) -> bool:
        with self.uow:
            existing_job = self.uow.jobs.get(id_)
            if not existing_job:
                return False
            job.__dict__.update(owner_id=owner_id)
            existing_job.update(job.__dict__)
            self.uow.commit()
        return True

    def delete_job_by_id(self, id_: int) -> bool:
        with self.uow:
            existing_job = self.uow.jobs.get(id_)
            if not existing_job:
                return False
            existing_job.delete(synchronize_session=False)
            self.uow.commit()
        return True

    def search_job(self, query: str) -> list[JobOutputDto]:
        with self.uow:
            return self.uow.jobs.search(query)
