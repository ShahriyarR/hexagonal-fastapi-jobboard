from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates

from src.jobboard.adapters.entrypoints.api.v1.route_login import (
    get_current_user_from_token,
)
from src.jobboard.domain.model.model import User
from src.jobboard.domain.ports.job_service import JobService
from src.jobboard.domain.schemas.jobs import JobCreateInputDto, JobOutputDto
from src.jobboard.main.containers import Container

router = APIRouter()
templates = Jinja2Templates(directory="src/jobboard/adapters/entrypoints/templates")


@router.post("/create-job/", response_model=JobOutputDto)
@inject
def create_job(
    job: JobCreateInputDto,
    current_user: User = Depends(get_current_user_from_token),
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    return job_service.create(job=job, owner_id=current_user.id)


@router.get(
    "/get/{id}", response_model=JobOutputDto
)  # if we keep just "{id}" . it would stat catching all routes
@inject
def read_job(
    id: int,
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    job = job_service.retrieve_job(id_=id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with this id {id} does not exist",
        )
    return job


@router.get("/all", response_model=list[JobOutputDto])
@inject
def read_jobs(
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    return job_service.list_jobs()


@router.put("/update/{id}")
@inject
def update_job(
    id: int,
    job: JobCreateInputDto,
    current_user: User = Depends(get_current_user_from_token),
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    # TODO: this is still not obvious why we are updating the owner id, just grabbed from original repo.
    message = job_service.update_job_by_id(id_=id, job=job, owner_id=current_user.id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {id} not found"
        )
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{id}")
@inject
def delete_job(
    id: int,
    current_user: User = Depends(get_current_user_from_token),
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    job = job_service.retrieve_job(id_=id)
    if not job:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id {id} does not exist",
        )
    if job.owner_id == current_user.id or current_user.is_super_user:
        job_service.delete_job_by_id(id_=id)
        return {"detail": "Successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted!!!!"
    )


@router.get("/autocomplete")
@inject
def autocomplete(
    term: Optional[str] = None,
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    jobs = job_service.search_job(term)
    return [job.title for job in jobs]
