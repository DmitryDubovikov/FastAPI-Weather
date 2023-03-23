from src.database import Base
from sqlalchemy import MetaData

metadata = MetaData()

from fastapi_users.db import SQLAlchemyBaseUserTableUUID


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
