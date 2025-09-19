from typing import (
    Callable,
    Dict,
    Any,
    Awaitable
)
from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_factory):
        super().__init__()
        self.session_factory = session_factory
    
    async def __call__(
            self,
            handler: Callable[[Dict[str, Any], Any], Awaitable[Any]],
            event: Any,
            data: Dict[str, Any]
    ) -> Any:
        async with self.session_factory() as session:
            data['session'] = session  # <- кладём в data
            return await handler(event, data)
