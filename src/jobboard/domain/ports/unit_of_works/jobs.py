import abc

from src.jobboard.domain.ports.common import messagebus
from src.jobboard.domain.ports.repositories.jobs import JobRepositoryInterface


class JobUnitOfWorkInterface(abc.ABC):
    jobs: JobRepositoryInterface

    def __enter__(self) -> "JobUnitOfWorkInterface":
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()
        self.publish_events()

    def publish_events(self):
        for job in self.jobs.seen:
            while job.events:
                event = job.events.pop(0)
                messagebus.handle(event)

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
