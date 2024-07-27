from aiogram.filters import BaseFilter
from aiogram.types import Message

from config_reader import config, TRADER_TOOLS
from db.models import User


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in config.ADMINS_ID:
            return True

class TraderFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs) -> bool:
        user = await User.get_or_none(user_id=message.from_user.id)
        if user:
            if user.state == 3:
                await message.answer("Пока ваша торговля не окончена вы не можете использовать новые сигналы!")
                return False
            elif user.state == 4:
                await message.answer("Нажмите на кнопку Выигрыш или Проигрыш")
                return False
            elif user.state == 5:
                await message.answer("Бот анализирует рынок")
                return False
        return True