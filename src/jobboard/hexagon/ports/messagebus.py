from typing import Callable, Type

from src.jobboard.hexagon.model import events


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_user_created_notification(event: events.UserCreated):
    print(f"User created {event.user_name}")


def send_job_created_notification(event: events.JobCreated):
    print(f"Job created {event.title}")


HANDLERS = {
    events.UserCreated: [send_user_created_notification],
    events.JobCreated: [send_job_created_notification],
}  # type: dict[Type[events.Event], list[Callable]]
