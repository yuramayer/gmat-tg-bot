"""Async database connection and session management"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Database:
    """Async database connection manager"""

    def __init__(
            self,
            db_url: str
            ):
        """
        Initialize the Database object
        
        Args:
            db_url: uniform resource locator 
                for the PostgreSQL DB
        """
        self._engine = create_async_engine(
            db_url,
            echo=False,
            future=True
        )
        self._session_factory = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
    
    async def get_session(self) -> AsyncSession:
        """Return new async session"""
        return self._session_factory()

    async def init_models(self):
        """Creates tables if they don't exist"""
        async with self._engine.begin() as conn:
            await conn.run_sync(
                Base.metadata.create_all
            )
