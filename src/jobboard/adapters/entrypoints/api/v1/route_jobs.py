import json
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates

from src.jobboard.adapters.entrypoints import STATUS_CODES
from src.jobboard.adapters.entrypoints.api.v1.route_login import (
    get_current_user_from_token,
)
from src.jobboard.domain.model.model import User
from src.jobboard.domain.ports.job_service import JobService
from src.jobboard.domain.ports.responses import ResponseTypes
from src.jobboard.domain.schemas.jobs import JobCreateInputDto
from src.jobboard.configurator.containers import Container

router = APIRouter()
templates = Jinja2Templates(directory="src/jobboard/adapters/entrypoints/templates")


@router.post("/create-job/")
@inject
def create_job(
    job: JobCreateInputDto,
    current_user: User = Depends(get_current_user_from_token),
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    response = job_service.create(job=job, owner_id=current_user.id)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.get("/get/{id}")  # if we keep just "{id}" . it would stat catching all routes
@inject
def read_job(
    id: int,
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    response = job_service.retrieve_job(id_=id)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.get("/all")
@inject
def read_jobs(
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    response = job_service.list_jobs()
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.put("/update/{id}")
@inject
def update_job(
    id: int,
    job: JobCreateInputDto,
    current_user: User = Depends(get_current_user_from_token),
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    response = job_service.update_job_by_id(id_=id, job=job, owner_id=current_user.id)
    data = jsonable_encoder(response.value)
    return Response(
        content=json.dumps(data),
        media_type="application/json",
        status_code=STATUS_CODES[response.type],
    )


@router.delete("/delete/{id}")
@inject
def delete_job(
    id: int,
    current_user: User = Depends(get_current_user_from_token),
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    response = job_service.retrieve_job(id_=id)
    if response.type != ResponseTypes.SUCCESS:
        return Response(
            content=json.dumps(response.value),
            media_type="application/json",
            status_code=STATUS_CODES[response.type],
        )
    if response.value.owner_id == current_user.id or current_user.is_super_user:
        response = job_service.delete_job_by_id(id_=id)
        return Response(
            content=json.dumps(response.value),
            media_type="application/json",
            status_code=STATUS_CODES[response.type],
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted"
    )


@router.get("/autocomplete")
@inject
def autocomplete(
    term: Optional[str] = None,
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    jobs = job_service.search_job(term)
    return [job.title for job in jobs]
