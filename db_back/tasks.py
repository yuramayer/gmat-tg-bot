"""SQL Async funcs working with the questions"""

from db import get_pool
from db_back.users import get_user_id


async def get_new_task_for_user(
        telegram_id: int
        ) -> dict | None:
    """
    Find and return a new task that the user hasn't answered yet.

    Args:
        telegram_id (int): Telegram ID of the user.

    Returns:
        dict | None: A dictionary with task data (id, question,
        options, correct), or None if no new tasks available.
    """
    pool = get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            SELECT t.id, t.question, t.options, t.correct
            FROM gmat_tasks t
            WHERE t.id NOT IN (
                SELECT task_id
                FROM user_tasks ut
                JOIN users u ON ut.user_id = u.id
                WHERE u.telegram_id = $1
            )
            ORDER BY RANDOM()
            LIMIT 1;
        """, telegram_id)
        return dict(row) if row else None


async def save_user_answer(
        telegram_id: int,
        task_id: int, user_answer: str
        ) -> None:
    """
    Save the user's answer for a specific task.

    Args:
        telegram_id (int): Telegram ID of the user.
        task_id (int): ID of the task being answered.
        user_answer (str): The answer provided by the user.

    Raises:
        ValueError: If the user is not found in the database.
    """
    user_id = await get_user_id(telegram_id)
    if not user_id:
        raise ValueError(f"User with telegram_id {telegram_id} not found")

    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO user_tasks (
                           user_id, task_id, status,
                           user_answer, answered_at
                           )
            VALUES ($1, $2, 'answered', $3, now());
        """, user_id, task_id, user_answer)
