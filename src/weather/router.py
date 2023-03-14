from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import City, Weather
from .schemas import CitySchema, WeatherSchema

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/cities", response_model=List[CitySchema])
async def get_cities(session: AsyncSession = Depends(get_async_session)):
    stmt = select(City)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/city/{city_name}", response_model=CitySchema)
async def get_city(city_name: str, session: AsyncSession = Depends(get_async_session)):
    stmt = select(City).where(City.name == city_name)
    result = await session.execute(stmt)
    return result.scalars().first()


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
