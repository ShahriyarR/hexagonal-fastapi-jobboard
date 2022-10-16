from apis.version1.route_login import login_for_access_token
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.jobboard.adapters.entrypoints.webapps.auth.forms import LoginForm
from src.jobboard.domain.ports.user_service import UserService
from src.jobboard.main.containers import Container

templates = Jinja2Templates(directory="src/jobboard/adapters/entrypoints/templates")
router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login/")
@inject
async def login(request: Request, user_service: UserService = Depends(Provide[Container.user_service])):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)
