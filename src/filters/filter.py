from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from config_reader import config, TRADER_TOOLS
from db.models import User


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in config.ADMINS_ID:
            return True

class TraderFilter(BaseFilter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        user = await User.get_or_none(user_id=message.from_user.id)
        if user:
            if user.state != 3:
                return True
            if isinstance(message, Message):
                await message.answer("Пока ваша торговля не окончена вы не можете использовать новые сигналы!")
            else:
                await message.message.answer("Пока ваша торговля не окончена вы не можете использовать новые сигналы!")
        return False
            