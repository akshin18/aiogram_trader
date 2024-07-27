import datetime
import asyncio
import random
from typing import Union

from aiogram.types import Message, ChatJoinRequest
from loguru import logger

from config_reader import TRADER_TOOLS, config, google_sheet, indicator_form, time_splitter
from db.models import User
from app import bot
from keyboards.common import get_inline_keyboard, get_keyboard


async def req_user(message: Union[Message, ChatJoinRequest], req=False):
    user, created = await User.get_or_create(
        name=message.from_user.full_name,
        username=message.from_user.username,
        user_id=message.from_user.id,
    )
    if created:
        logger.info(f"New user: {user.name}")
        now = datetime.datetime.now(google_sheet.moscow_timezone).strftime("%d/%m/%Y, %H:%M:%S")
        google_sheet.create_user(now, now, user.user_id, True, user.username)
    if user.state == 0:
        await message.answer(f"Подпишитесь на канал (напишите мне в личку: {message.from_user.id} , я выдам доступ)")
        return
    elif user.state == 1:
        if not user.trader_id:
            await message.answer("Отправьте ваш ид пользователя в таком формате: 123456789")
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
    user.signals_count += 1
    google_sheet.update_indecator_count(user.user_id, user.signals_count)
    text = indicator_form % (trade_tools, trade_time_str, random.choice(["Понижение📉", "Повышение📈"]))
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
                await bot.send_message(user.user_id,f"Какой вы получили результат по последней сделке {user.trade_choose_tools}?", reply_markup=get_inline_keyboard(["Выигрыш", "Проигрыш"], 1))
        await asyncio.sleep(10)


async def generate_random_trade(user: User, message: Message):
    random_trade_type = random.choice(list(TRADER_TOOLS.keys()))
    random_trade_tool = random.choice(TRADER_TOOLS[random_trade_type]['tools'])
    trade_time = TRADER_TOOLS[random_trade_type].get('time')
    if trade_time and len(trade_time) > 3:
        random_trade_time_str = random.choice(trade_time)
    else:
        random_trade_time_str = "15 секунд"
    user.trade_type = random_trade_type
    user.trade_choose_tools = random_trade_tool
    user.trade_time = random_trade_time_str
    user.auto_trade_count += 1
    await user.save()
    text = f"""Выберите торговую пару :
{random_trade_tool}
В опции: {random_trade_type}
Время эксперации: {random_trade_time_str}"""
    inline_keyboard = get_inline_keyboard("Подтверждаю выбор нужных данных!", custom=["agree_auto_trade"])
    await message.answer(text, reply_markup=inline_keyboard)

async def is_auto_trade(user: User, message: Message):
    if user.trade_mode == 1:
        if user.auto_trade_count < user.auto_trade_choose_count:
            user.trade_start_time += datetime.timedelta(minutes=3)
            user.state = 5
            await user.save()
            await asyncio.sleep(60)
            user.state = 2
            await user.save()
            await generate_random_trade(user, message)
            return True
        user.auto_trade_choose_count = 0
        user.auto_trade_count = 0
        await user.save()
    