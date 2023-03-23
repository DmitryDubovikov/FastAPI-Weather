from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, text
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import gather
from aiohttp import ClientSession
from src.config import API_KEY
from src.auth.base_config import fastapi_users
from pydantic import parse_obj_as


from src.database import get_async_session
from .models import City, Weather
from .schemas import (
    CitySchema,
    WeatherSchema,
    ResponseWeatherSchema,
    ResponseCityStatsSchema,
    ListResponseCityStatsSchema,
)


router = APIRouter(prefix="/weather", tags=["Weather"])

current_user = fastapi_users.current_user()


@router.get("/cities", response_model=List[CitySchema])
async def get_cities(session: AsyncSession = Depends(get_async_session)):
    stmt = select(City)
    result = await session.execute(stmt)
    return result.scalars().all()


@router.post("/{city_name}")
async def add_city(
    city_name: str,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    # TODO: добавить проверку, что город есть в openweathermap
    stmt = insert(City).values(name=city_name)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/last-weather/", response_model=List[ResponseWeatherSchema])
async def get_last_weather(
    search: str = "",
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    """
    Get last (most recent available) weather for each city. Use 'search' parameter to filter among cities.
    """
    qstr = """
    SELECT city, temperature, pressure, wind, date_trunc('second', time) as time
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
    result_list = result.all()
    return parse_obj_as(List[ResponseWeatherSchema], result_list)


@router.get("/city-stats/", response_model=List[ResponseCityStatsSchema])
async def get_city_stats(
    city_name: str,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
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


@router.post("/fetch-weather/")
async def fetch_weather(
    session: AsyncSession = Depends(get_async_session), user=Depends(current_user)
):
    """
    Fetch weather data from openweathermap and POST weather (for each city).
    """
    stmt = select(City)
    result = await session.execute(stmt)
    cities = {el.id: el.name for el in result.scalars().all()}
    inv_cities = {value: key for key, value in cities.items()}

    async with ClientSession() as client_session:

        data = await gather(
            *[
                fetch(
                    client_session,
                    f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid="
                    + API_KEY,
                    city,
                )
                for city in cities.values()
            ]
        )

    body = [
        {
            "city_id": inv_cities.get(el["city"]),
            "temperature": el["temperature"],
            "pressure": el["pressure"],
            "wind": el["wind"],
        }
        for el in data
    ]
    print(body)

    await session.execute(insert(Weather), body)
    await session.commit()

    return {"status": "success"}


async def fetch(session, url, city):
    async with session.get(url) as response:
        data = await response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "pressure": data["main"]["pressure"],
            "wind": data["wind"]["speed"],
        }
