import uuid
import uvicorn
from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.schemas import UserCreate, UserRead
from auth.manager import get_user_manager
from database import User

app = FastAPI(title="My FastAPI App")


@app.get("/")
async def hello():
    return {"message": "Hello World!"}


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, unauthenticated user"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
