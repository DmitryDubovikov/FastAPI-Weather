from fastapi import APIRouter, BackgroundTasks, Depends
from src.auth.base_config import current_user
from src.weather.router import get_last_weather
from .tasks import (
    send_email_last_weather_background_tasks,
    send_email_last_weather_celery,
)

router = APIRouter(prefix="/report", tags=["Reports"])


@router.get("/last-weather-background")
def get_last_weather_email_background(
    background_tasks: BackgroundTasks,
    weather_data=Depends(get_last_weather),
    user=Depends(current_user),
):
    background_tasks.add_task(
        send_email_last_weather_background_tasks,
        [el.dict() for el in weather_data],
        user.email,
    )
    return {"status": 200, "data": "Email sent", "details": "with background_tasks"}


@router.get("/last-weather-celery")
def get_last_weather_email_celery(
    weather_data=Depends(get_last_weather), user=Depends(current_user)
):
    send_email_last_weather_celery.delay([el.dict() for el in weather_data], user.email)
    return {"status": 200, "data": "Email sent", "details": "with celery"}
