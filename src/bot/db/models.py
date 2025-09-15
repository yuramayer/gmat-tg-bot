"""ORM models"""

from sqlalchemy import (
    Column,
    Integer,
    String
)
from src.bot.db.session import Base


class User(Base):
    """"Object for the Users table"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=True)
