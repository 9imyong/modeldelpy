from fastapi import FastAPI, Request, Form, Depends
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi_csrf_protect import CsrfProtect
from pydantic import BaseModel

from config.settings import settings
from utils.security import verify_password
from routers.models import router as models_router

# CSRF 설정
@CsrfProtect.load_config
def get_csrf_config():
    class CsrfSettings(BaseModel):
        secret_key: str = settings.CSRF_SECRET
    return CsrfSettings()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.CSRF_SECRET)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(models_router)
templates = Jinja2Templates(directory="templates")

# 로그인 페이지
@app.get("/", include_in_schema=False)
async def login_page(request: Request, csrf_protect: CsrfProtect = Depends()):
    token = csrf_protect.generate_csrf()
    return templates.TemplateResponse("index.html", {"request": request, "csrf_token": token})

@app.post("/login", include_in_schema=False)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    csrf_protect: CsrfProtect = Depends()
):
    csrf_protect.validate_csrf(request)
    if username == settings.ADMIN_USERNAME and verify_password(password, settings.ADMIN_PASSWORD_HASH):
        return RedirectResponse(url="/models", status_code=302)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "error": "로그인 실패", "csrf_token": csrf_protect.generate_csrf()},
        status_code=401
    )