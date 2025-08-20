"""Filters for the bot"""

from aiogram.filters import Filter
from aiogram.types import Message


class IsAdmin(Filter):
    """Filter checks if user is admin"""
    def __init__(self, admins_ids):
        self.admins_ids = admins_ids

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins_ids


class NotAdmin(Filter):
    """Filter checks if user is not an admin"""
    def __init__(self, admins_ids):
        self.admins_ids = admins_ids

    async def __call__(self, message: Message):
        return message.from_user.id not in self.admins_ids
