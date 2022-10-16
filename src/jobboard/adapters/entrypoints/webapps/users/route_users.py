from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError

from src.jobboard.adapters.entrypoints.webapps.users.forms import UserCreateForm
from src.jobboard.domain.ports.user_service import UserService
from src.jobboard.domain.schemas.users import UserCreateInputDto
from src.jobboard.main.containers import Container

templates = Jinja2Templates(directory="src/jobboard/adapters/entrypoints/templates")
router = APIRouter(include_in_schema=False)


@router.get("/register/")
def register(request: Request):
    return templates.TemplateResponse("users/register.html", {"request": request})


@router.post("/register/")
@inject
async def register(
    request: Request,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreateInputDto(
            user_name=form.username, email=form.email, password=form.password
        )
        try:
            user = user_service.create(user=user)
            return responses.RedirectResponse(
                "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
            )  # default is post request, to use get request added status code 302
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate username or email")
            return templates.TemplateResponse("users/register.html", form.__dict__)
    return templates.TemplateResponse("users/register.html", form.__dict__)
