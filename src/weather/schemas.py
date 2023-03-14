from datetime import datetime
from pydantic import BaseModel


class CitySchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class WeatherSchema(BaseModel):
    city_id: int
    temperature: float
    pressure: int
    wind: int


class ResponseWeatherSchema(BaseModel):
    city: str
    temperature: float
    pressure: int
    wind: int
    time: datetime

    class Config:
        orm_mode = True


class ResponseCityStatsSchema(BaseModel):
    city: str
    time: datetime
    temperature: float
    avg_temperature: float
    pressure: int
    avg_pressure: int
    wind: int
    avg_wind: int
    time: datetime

    class Config:
        orm_mode = True
