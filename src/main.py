from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

from src.auth.models import User

from src.weather.router import router as router_weather
from src.tasks.router import router as router_tasks
from src.pages.router import router as router_pages

app = FastAPI(title="My FastAPI App")

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

current_user = fastapi_users.current_user()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_weather)
app.include_router(router_tasks)
app.include_router(router_pages)
