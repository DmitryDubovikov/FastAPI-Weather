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
    # TODO: передавать в background_tasks что-то адекватнее, чем str(weather_data)
    background_tasks.add_task(
        send_email_last_weather_background_tasks, str(weather_data), user.email
    )
    return {"status": 200, "data": "Email sent", "details": "with background_tasks"}


@router.get("/last-weather-celery")
def get_last_weather_email_celery(
    weather_data=Depends(get_last_weather), user=Depends(current_user)
):
    # TODO: передавать в celery что-то адекватнее, чем str(weather_data)
    send_email_last_weather_celery.delay(str(weather_data), user.email)
    return {"status": 200, "data": "Email sent", "details": "with celery"}
