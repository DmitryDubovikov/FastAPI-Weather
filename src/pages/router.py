from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.weather.router import get_last_weather

router = APIRouter(prefix="/pages", tags=["Pages"])

templates = Jinja2Templates(directory="src/templates")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/last-weather/")
def get_search_page(request: Request, weather_data=Depends(get_last_weather)):
    return templates.TemplateResponse(
        "last.html", {"request": request, "weather_data": weather_data}
    )
