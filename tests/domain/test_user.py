from src.jobboard.hexagon.model.events import Event, UserCreated
from src.jobboard.hexagon.model.model import (
    User,
    user_model_event_factory,
    user_model_factory,
)


def test_create_user_model_from_dict(get_user_model_dict):
    user = User.from_dict(get_user_model_dict)
    get_user_model_dict["events"] = []
    get_user_model_dict["jobs"] = set()
    assert get_user_model_dict == user.to_dict()


def test_create_user_model_event_factory(get_user_model_dict):
    del get_user_model_dict["uuid"]
    user = user_model_event_factory(**get_user_model_dict)
    assert len(user.events) == 1
    assert type(user.events[0]) is UserCreated


def test_create_user_model_factory(get_user_model_dict):
    del get_user_model_dict["uuid"]
    metric = user_model_factory(**get_user_model_dict)
    assert metric.events == []


def test_create_user_model_event(get_user_model_dict):
    del get_user_model_dict["uuid"]
    metric = user_model_event_factory(**get_user_model_dict)
    assert len(metric.events) == 1
    assert type(metric.events[0]) is UserCreated
    event = metric.events[0]
    assert isinstance(event, Event)
    assert event.uuid == metric.uuid


def test_create_metric_event_from_dict(get_user_model_dict):
    event = UserCreated.from_dict(get_user_model_dict)
    assert event.to_dict() == get_user_model_dict


def test_if_users_are_identical(get_user_model_dict):
    user1 = User.from_dict(get_user_model_dict)
    get_user_model_dict["user_name"] = "fake"
    user2 = User.from_dict(get_user_model_dict)
    assert user1 != user2
    assert user1 != get_user_model_dict
