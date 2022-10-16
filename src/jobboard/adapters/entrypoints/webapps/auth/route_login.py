from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates

from src.jobboard.adapters.entrypoints.api.v1.route_login import login_for_access_token
from src.jobboard.adapters.entrypoints.webapps.auth.forms import LoginForm

templates = Jinja2Templates(directory="src/jobboard/adapters/entrypoints/templates")
router = APIRouter(include_in_schema=False)


@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login/")
async def login(
    request: Request,
):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            login_for_access_token(response=response, form_data=form)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)
