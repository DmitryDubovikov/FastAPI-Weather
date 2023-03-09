from datetime import datetime
from pydantic import BaseModel


class CitySchema(BaseModel):
    # id: int
    name: str


class WeatherSchema(BaseModel):
    city_id: int
    temperature: float
    pressure: int
    wind: int
