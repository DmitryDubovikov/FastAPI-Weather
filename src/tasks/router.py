from fastapi import APIRouter, BackgroundTasks, Depends

from src.auth.base_config import current_user

from .tasks import send_email_lowest_temperatures, send_email_highest_temperatures

router = APIRouter(prefix="/report", tags=["Reports"])


@router.get("/lowest-temperatures")
def get_lowest_temperatures_email(
    background_tasks: BackgroundTasks, user=Depends(current_user)
):
    # TODO: добавить получение данных из базы, добавить async
    background_tasks.add_task(send_email_lowest_temperatures, user.email)
    return {"status": 200, "data": "Email sent", "details": "with background_tasks"}


@router.get("/highest-temperatures")
def get_highest_temperatures_email():
    # TODO: добавить получение данных из базы, добавить async
    send_email_highest_temperatures.delay()
    return {"status": 200, "data": "Email sent", "details": "with celery"}
