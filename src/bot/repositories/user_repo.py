"""Repository for working with users"""

from sqlalchemy.ext.asyncio import AsyncSession
from src.bot.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    

    async def get_by_tg_id(
            self,
            tg_id: int
            ) -> User | None:
        stmt = await self.session.get(User, tg_id)
        return stmt
    
    async def create(
            self,
            tg_id: int,
            name: str
            ) -> User:
        user = User(tg_id=tg_id, name=name)
        self.session.add(user)
        await self.session.commit()
        return user
