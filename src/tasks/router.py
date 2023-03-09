from fastapi import APIRouter, BackgroundTasks, Depends

from src.auth.base_config import current_user

from .tasks import send_email_lowest_temperatures

router = APIRouter(prefix="/report", tags=["Reports"])


@router.get("/lowest-temperatures")
def get_lowest_temperatures_email(background_tasks: BackgroundTasks):
    # TODO: добавить получение данных из базы, добавить async
    background_tasks.add_task(send_email_lowest_temperatures)
    return {"status": 200, "data": "Email sent", "details": None}
