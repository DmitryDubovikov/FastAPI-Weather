from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import City, Weather
from .schemas import (
    CitySchema,
    WeatherSchema,
    ResponseWeatherSchema,
    ResponseCityStatsSchema,
)

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


@router.get("/last_weather/", response_model=List[ResponseWeatherSchema])
async def get_last_weather(
    search: str = "", session: AsyncSession = Depends(get_async_session)
):
    """
    Get last (most recent available) weather for each city. Use 'search' parameter to filter among cities.
    """
    qstr = """
    SELECT city, temperature, pressure, wind, time
    FROM
    (SELECT 
            city_id,
            city.name as city,
            time,
            temperature,
            pressure,
            wind,
            Row_number() OVER (PARTITION BY city_id
                                ORDER BY TIME DESC) AS r_num
    FROM public.weather
    INNER JOIN city ON city.id = weather.city_id
    AND TRUE) AS decorated
    WHERE r_num = 1
    """
    if search:
        qstr = qstr.replace("AND TRUE", f"AND city.name like '%{search}%'")
    else:
        qstr = qstr.replace("AND TRUE", "")
    result = await session.execute(text(qstr))
    return result.all()


@router.get("/city_stats/", response_model=List[ResponseCityStatsSchema])
async def get_city_stats(
    city_name: str, session: AsyncSession = Depends(get_async_session)
):
    """
    Get weather data and average values for 'city_name' city.
    """
    # TODO: добавить отбор по периоду
    qstr = f"""    
    SELECT city.name as city,
       temperature,
       time,
	   AVG(temperature) OVER (PARTITION BY city.name) as avg_temperature,
       pressure,
	   AVG(pressure) OVER (PARTITION BY city.name) as avg_pressure,
       wind,
	   AVG(wind) OVER (PARTITION BY city.name) as avg_wind
    FROM city
    INNER JOIN weather ON city.name = '{city_name}'
    AND city.id = weather.city_id
    """
    result = await session.execute(text(qstr))
    return result.all()
