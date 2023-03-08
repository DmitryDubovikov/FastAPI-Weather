from fastapi import FastAPI, Depends

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

from src.auth.models import User

from src.weather.router import router as router_weather

app = FastAPI(title="My FastAPI App")

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


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, unauthenticated user"
