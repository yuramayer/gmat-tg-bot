"""SQL Async funcs working with the users"""

from db import get_pool


async def register_user(
        telegram_id: int,
        username: str,
        full_name: str
        ) -> None:
    """
    Add a new user to the database if not already exists.

    Args:
        telegram_id (int): Telegram user ID.
        username (str): Telegram username.
        full_name (str): Telegram full name.

    Returns:
        None
    """
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (telegram_id, username, full_name)
            VALUES ($1, $2, $3)
            ON CONFLICT (telegram_id) DO NOTHING;
        """, telegram_id, username, full_name)


async def get_user_id(telegram_id: int) -> int | None:
    """
    Get the internal user ID by Telegram ID.

    Args:
        telegram_id (int): Telegram user ID.

    Returns:
        int | None: ID of the user in the database, or None if not found.
    """
    pool = get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT id FROM users WHERE telegram_id = $1;
        """, telegram_id)
        return row["id"] if row else None
