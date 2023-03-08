from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

Base = declarative_base()


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    weathers = relationship("Weather", back_populates="city")


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True)
    city_id = Column(ForeignKey("city.id"))
    city = relationship("City", back_populates="weathers")
    temperature = Column(Float)
    pressure = Column(Integer)
    wind = Column(Float)
    time = Column(DateTime, server_default=func.now())


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
