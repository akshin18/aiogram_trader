from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from loguru import logger

from config_reader import config, TRADER_TOOLS
from db.models import User
from keyboards.common import get_inline_keyboard
from utils import language


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in config.ADMINS_ID:
            return True

class TraderFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs) -> bool:
        user = await User.get_or_none(user_id=message.from_user.id)
        if user:
            is_member = await check_subscription(message.bot, message.from_user.id)
            if not is_member:
                await message.answer(language.new_sub_to_channel[config.LANG], reply_markup=get_inline_keyboard(language.i_have_subscribed[config.LANG], custom=["i_have_subscribed"]))
                return False
            if user.state == 0:
                user.state = 1
                await user.save()
                return True
            if user.state == 3:
                await message.answer(language.wait_trading_done[config.LANG])
                return False
            elif user.state == 4:
                if message.text in language.trading_methods[config.LANG]:
                    await message.answer(language.click_win_or_lose[config.LANG], reply_markup=get_inline_keyboard(language.trade_result_types[config.LANG], 1))
                    return False
            elif user.state == 5:
                await message.answer(language.bot_analizing_please_wait[config.LANG])
                return False
        return True
    
async def check_subscription(bot: Bot, user_id: int):
    member = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=user_id)
    if member.status != ChatMemberStatus.LEFT:
        return True
    
