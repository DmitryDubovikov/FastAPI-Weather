from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import City, Weather
from .schemas import CitySchema, WeatherSchema

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/")
async def get_cities(session: AsyncSession = Depends(get_async_session)):
    stmt = select(City)
    result = await session.scalars(stmt)
    data = []
    for city in result:
        data.append({"id": city.id, "name": city.name})
    return {"cities": data}


@router.post("/{city_name}")
async def add_city(city_name: str, session: AsyncSession = Depends(get_async_session)):
    # TODO: добавить проверку, что город есть в openweathermap
    stmt = insert(City).values(name=city_name)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.post("/")
async def add_weather(
    weather_data: WeatherSchema, session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Weather).values(**weather_data.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
