"""Async PostgreSQL connection pool for the whole bot."""

import asyncpg
from config.conf import (
    DB_USER,
    DB_PASS,
    DB_NAME,
    DB_HOST,
    DB_PORT
)

_pool: asyncpg.Pool = None


async def init_db() -> None:
    """
    Create a connection pool to the PostgreSQL database.

    This function should be called once when the bot starts.

    Returns:
        None
    """
    global _pool  # pylint: disable=global-statement
    _pool = await asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT,
        min_size=1,
        max_size=5
    )


def get_pool() -> asyncpg.Pool:
    """
    Get the connection pool object.

    Returns:
        asyncpg.Pool: The current PostgreSQL connection pool.
    """
    return _pool
