import datetime
import asyncio
import random
from typing import Union
from traceback import format_exc

from aiogram.types import Message, ChatJoinRequest, ContentType
from loguru import logger
import pytz

from config_reader import config, google_sheet, indicator_form, time_splitter
from db.models import User
from app import bot
from keyboards.common import get_inline_keyboard, get_keyboard


async def req_user(message: Union[Message, ChatJoinRequest], req=False):
    user, created = await User.get_or_create(
        name=message.from_user.full_name,
        username=message.from_user.username,
        user_id=message.from_user.id,
    )
    # add_user_to_sheet(user)
    if user.state == 0:
        await message.answer(f"Подпишитесь на канал (напишите мне в личку: {message.from_user.id} , я выдам доступ)")
        return
    elif user.state == 1:
        if not user.trader_id:
            await message.answer("Отправьте ваш ид пользователя Exnova в таком формате: 123456789")
        else:
            user.state = 2
            await user.save()
    elif user.state == 2:
        menu = get_keyboard(["Ручной трейдинг", "Управляемый трейдинг"])
        await message.answer("Меню:", reply_markup=menu)



def add_user_to_sheet(user: User):
    google_sheet.create_user(
        user.created_at.strftime("%d/%m/%Y"),
        user.created_at.strftime("%H:%M"),
        user.user_id,
        username=user.username,
    )

async def set_subscribed(user_id: int):
    user = await User.get_or_none(user_id=user_id)
    if user:
        user.state = 1
        await user.save()

async def set_paid(user_id: int):
    user = await User.get_or_none(user_id=user_id)
    if user:
        user.is_paid = True
        await user.save()


async def send_indicator(message: Message, user: User, trade_tools: str, trade_time: int, trade_time_str: str = "15 секунд"):
    text = indicator_form % (trade_tools, trade_time_str, random.choice(["Понижение", "Повышение"]))
    user.state = 3
    trade_delay = (trade_time + 15)
    user.trade_choose_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=trade_delay)
    user.trade_start_time = datetime.datetime.now(datetime.UTC)
    await user.save()
    await message.answer(text)
    await asyncio.sleep(trade_delay)
    user.state = 4
    await user.save()
    await message.answer(f"Какой вы получили результат по последней  сделке ({user.trade_choose_tools})?", reply_markup=get_inline_keyboard(["Выигрыш", "Проигрыш"], 1))


async def check_forgotten():
    while True:
        users = await User.filter(state=3)
        logger.debug(f"{len(users)=}")
        for user in users:
            now = datetime.datetime.now(datetime.UTC)
            if user.trade_start_time + datetime.timedelta(seconds=time_splitter.get(user.trade_time, 15) + 15) < now:
                user.state = 4
                await user.save()
                await bot.send_message(user.user_id,f"Какой вы получили результат по последней  сделке {user.trade_choose_tools}?", reply_markup=get_inline_keyboard(["Выигрыш", "Проигрыш"], 1))
        await asyncio.sleep(10)