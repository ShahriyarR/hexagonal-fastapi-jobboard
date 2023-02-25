from loguru import logger

from typing import Callable
from src.jobboard.domain.model import events


def handle(event: events.Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_user_created_notification(event: events.UserCreated):
    with logger.contextualize(request_id="SEND_USER_CREATED_NOTIFICATION"):
        logger.info(f"User created {event.user_name}")


def send_job_created_notification(event: events.JobCreated):
    with logger.contextualize(request_id="SEND_JOB_CREATED_NOTIFICATION"):
        logger.info(f"Job created {event.title}")


HANDLERS: dict[type[events.Event], list[Callable]] = {
    events.UserCreated: [send_user_created_notification],
    events.JobCreated: [send_job_created_notification],
}