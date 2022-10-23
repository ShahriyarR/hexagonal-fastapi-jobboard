from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, responses, status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates

from src.jobboard.adapters.entrypoints.api.v1.route_login import (
    get_current_user_from_token,
)
from src.jobboard.adapters.entrypoints.webapps.jobs.forms import JobCreateForm
from src.jobboard.hexagon.model.model import User
from src.jobboard.hexagon.ports.job_service import JobService
from src.jobboard.hexagon.schemas.jobs import JobCreateInputDto
from src.jobboard.configurator.containers import Container

templates = Jinja2Templates(directory="src/jobboard/adapters/entrypoints/templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
@inject
async def home(
    request: Request,
    job_service: JobService = Depends(Provide[Container.job_service]),
    msg: Optional[str] = None,
):
    jobs = job_service.list_jobs()
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "jobs": jobs, "msg": msg}
    )


@router.get("/details/{id}")
@inject
def job_detail(
    id: int,
    request: Request,
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    job = job_service.retrieve_job(id_=id)
    return templates.TemplateResponse(
        "jobs/detail.html", {"request": request, "job": job}
    )


@router.get("/post-a-job/")
def create_job(request: Request):
    return templates.TemplateResponse("jobs/create_job.html", {"request": request})


@router.post("/post-a-job/")
@inject
async def create_job(
    request: Request,
    job_service: JobService = Depends(Provide[Container.job_service]),
):
    form = JobCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param)
            job = JobCreateInputDto(**form.__dict__)
            job = job_service.create(job=job, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/details/{job.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("jobs/create_job.html", form.__dict__)
    return templates.TemplateResponse("jobs/create_job.html", form.__dict__)


@router.get("/delete-job/")
@inject
def show_jobs_to_delete(
    request: Request, job_service: JobService = Depends(Provide[Container.job_service])
):
    jobs = job_service.list_jobs()
    return templates.TemplateResponse(
        "jobs/show_jobs_to_delete.html", {"request": request, "jobs": jobs}
    )


@router.get("/search/")
@inject
def search(
    request: Request,
    job_service: JobService = Depends(Provide[Container.job_service]),
    query: Optional[str] = None,
):
    jobs = job_service.search_job(query)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "jobs": jobs}
    )
