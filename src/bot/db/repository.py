"""Repository for working with tables"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    AsyncResult
)
from src.bot.db.models import User


class UserRepository:
    """CRUD operations for Users object"""

    def __init__(
            self,
            session_factory: async_sessionmaker[AsyncSession]
        ):
        """
        Initialize the UserRepository object

        Args:
            session (async_sessionmaker): AsyncSession for the PostgreSQL
        """
        self._session_factory = session_factory
    
    async def get_by_tg_id(
            self,
            tg_id: int
        ) -> User | None:
        """
        Find user by Telegram ID
        
        Args:
            tg_id (int): user's telegram chat id
        
        Returns:
            User (optional): user's info
                from the 'users' table.
                If there's no user with such tg-id
                in the table, returns None
        """
        async with self._session_factory() as session:
            stmt = select(User).where(
                User.tg_id == tg_id)
            result: AsyncResult = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def add_user(
            self,
            tg_id: int,
            username: str
        ) -> User:
        """
        Add new user to the table
        
        Args:
            tg_id (int): user's telegram chat id
            username (str): telegram username
        
        Returns:
            User: user's info
                as from the 'users' table
        """
        async with self._session_factory() as session:
            user = User(
                tg_id=tg_id,
                username=username
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
