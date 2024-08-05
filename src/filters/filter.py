from aiogram.filters import BaseFilter
from aiogram.types import Message

from config_reader import config, TRADER_TOOLS
from db.models import User
from utils import language


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in config.ADMINS_ID:
            return True

class TraderFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs) -> bool:
        user = await User.get_or_none(user_id=message.from_user.id)
        if user:
            if user.state == 3:
                await message.answer(language.wait_trading_done[config.LANG])
                return False
            elif user.state == 4:
                if message.text in language.trading_methods[config.LANG]:
                    await message.answer(language.click_win_or_lose[config.LANG])
                    return False
            elif user.state == 5:
                await message.answer(language.bot_analizing_please_wait[config.LANG])
                return False
        return True