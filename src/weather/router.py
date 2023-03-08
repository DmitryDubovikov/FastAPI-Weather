from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .models import City
from .schemas import CitySchema

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/")
async def get_cities(session: AsyncSession = Depends(get_async_session)):
    stmt = select(City)
    result = await session.scalars(stmt)
    data = []
    for city in result:
        data.append(city.name)
    return {"cities": data}


@router.post("/")
async def add_city(
    new_city: CitySchema, session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(City).values(**new_city.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
