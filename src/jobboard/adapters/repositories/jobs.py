from src.jobboard.domain.model import model
from src.jobboard.domain.ports.repositories.jobs import JobRepositoryInterface


class JobSqlAlchemyRepository(JobRepositoryInterface):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, job):
        self.session.add(job)

    def _get(self, id_: int) -> model.Job:
        return self.session.query(model.Job).filter_by(id=id_).first()

    def _get_by_uuid(self, uuid: str) -> model.Job:
        return self.session.query(model.Job).filter_by(uuid=uuid).first()

    def _get_by_id_for_update(self, id_: int) -> model.Job:
        return self.session.query(model.Job).filter_by(id=id_)

    def _get_all(self) -> list[model.Job]:
        return self.session.query(model.Job).all()

    def _search(self, query: str) -> list[model.Job]:
        return self.session.query(model.Job).filter(model.Job.title.contains(query))
