from src.jobboard.domain.model.events import Event, JobCreated
from src.jobboard.domain.model.model import (
    Job,
    job_model_event_factory,
    job_model_factory,
)


def test_create_job_model_from_dict(get_job_model_dict):
    job = Job.from_dict(get_job_model_dict)
    get_job_model_dict["events"] = []
    assert get_job_model_dict == job.to_dict()


def test_create_job_model_event_factory(get_job_model_dict):
    del get_job_model_dict["uuid"]
    job = job_model_event_factory(**get_job_model_dict)
    assert len(job.events) == 1
    assert type(job.events[0]) is JobCreated


def test_create_job_model_factory(get_job_model_dict):
    del get_job_model_dict["uuid"]
    metric = job_model_factory(**get_job_model_dict)
    assert metric.events == []


def test_create_job_model_event(get_job_model_dict):
    del get_job_model_dict["uuid"]
    metric = job_model_event_factory(**get_job_model_dict)
    assert len(metric.events) == 1
    assert type(metric.events[0]) is JobCreated
    event = metric.events[0]
    assert isinstance(event, Event)
    assert event.uuid == metric.uuid


def test_create_metric_event_from_dict(get_job_model_dict):
    event = JobCreated.from_dict(get_job_model_dict)
    assert event.to_dict() == get_job_model_dict


def test_if_users_are_identical(get_job_model_dict):
    user1 = Job.from_dict(get_job_model_dict)
    get_job_model_dict["company"] = "fake"
    user2 = Job.from_dict(get_job_model_dict)
    assert user1 != user2
    assert user1 != get_job_model_dict
