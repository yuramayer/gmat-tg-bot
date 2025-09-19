from sqlalchemy.ext.asyncio import AsyncSession
from src.bot.repositories.user_repo import UserRepository

class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)
    
    async def get_or_create(
            self,
            tg_id: int,
            name: str
            ):
        user = await self.repo.get_by_tg_id(tg_id)
        if not user:
            user = await self.repo.create(
                tg_id=tg_id,
                name=name
            )
        return user
