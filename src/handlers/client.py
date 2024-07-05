import asyncio
import datetime
import random

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from loguru import logger

from config_reader import config, TRADER_TOOLS, time_splitter, lose_text
from filters.filter import TraderFilter
from utils.func import req_user, send_indicator
from keyboards.common import get_inline_keyboard, get_keyboard
from db.models import User
from utils.states import WinState


router = Router()
router.message.filter(TraderFilter())

@router.message(F.text == "/start")
async def req_handler(message: Message):
    await req_user(message, req=True)


@router.message(F.text == "id")
async def get_id(message: Message):
    await message.answer(str(message.from_user.id))


@router.message(F.text == "Ручной трейдинг")
async def manual_trading_handler(message: Message):
    user = await User.get_or_none(user_id=message.from_user.id)
    if user:
        if user.state == 3:
            return
        if not user.is_paid:
            await message.answer(config.FOR_PAY)
            return
        await message.answer("Опции:", reply_markup=get_inline_keyboard(list(TRADER_TOOLS.keys())))
        

@router.callback_query(F.data.in_(list(TRADER_TOOLS.keys())))
async def trading_type_callback(callback_query: CallbackQuery):
    await callback_query.message.delete()
    user = await User.get_or_none(user_id=callback_query.from_user.id)
    site = callback_query.data
    if user.trade_type == site and user.trade_choose_time is not None and user.trade_choose_time > datetime.datetime.now(datetime.UTC):
        random_trader_tools = user.trade_tools.split("&&")
    else:
        logger.debug(user.trade_choose_time)
        user.trade_type = site
        user.trade_choose_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=10*60)
        random_trader_tools = random.choices(TRADER_TOOLS[site]["tools"], k=5)
        user.trade_tools = "&&".join(random_trader_tools)
    await user.save()
    await callback_query.message.answer("Выберите инструмент трейдинга:", reply_markup=get_inline_keyboard(random_trader_tools, pre="tradingtype"))


@router.callback_query(F.data.startswith("tradingtype_"))
async def trade_tools_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    user = await User.get_or_none(user_id=callback_query.from_user.id)
    if user:
        trade_time = TRADER_TOOLS[user.trade_type]["time"]
        trade_choose_tools = callback_query.data.split("_", maxsplit=1)[1]
        user.trade_choose_tools = trade_choose_tools
        await user.save()
        if not trade_time:
            await send_indicator(callback_query.message, user, trade_choose_tools, 15)
            return
        await state.set_data({"tools": trade_choose_tools})
        await callback_query.message.answer("Опции:", reply_markup=get_inline_keyboard(trade_time, pre="tradetime"))


@router.callback_query(F.data.startswith("tradetime_"))
async def trade_time_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    user = await User.get_or_none(user_id=callback_query.from_user.id)
    if user:
        time_str = callback_query.data.split("_", maxsplit=1)[1]
        trade_time = time_splitter.get(time_str, 15)
        user.trade_time = time_str
        await user.save()
        data = await state.get_data()
        trade_tools = data["tools"]
        await send_indicator(callback_query.message, user, trade_tools, trade_time, callback_query.data.split("_", maxsplit=1)[1])


@router.message(F.text == "Управляемый трейдинг")
async def manual_trading_handler(message: Message):
    ...


@router.callback_query(F.data == "Выигрыш")
async def win_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.set_state(WinState.win)
    await callback_query.message.answer("Напишите сумму выигрыша")


@router.message(WinState.win)
async def win_count_handler(message: Message, state: FSMContext):
    user = await User.get_or_none(user_id=message.from_user.id)
    await state.clear()
    if user:
        await message.answer("Меню:", reply_markup=get_keyboard(["Ручной трейдинг", "Управляемый трейдинг"]))


@router.callback_query(F.data == "Проигрыш")
async def win_handler(callback_query: CallbackQuery):
    await callback_query.message.delete()
    user = await User.get_or_none(user_id=callback_query.from_user.id)
    if user:
        if user.lose_count >= 2:
            await callback_query.message.answer(lose_text, reply_markup=get_inline_keyboard("Я подтверждаю обновление страницы Экснова и выбор новой пары для трейдинга !", custom=["agree_lose"]))
        else:
            user.lose_count += 1
            await user.save()
            await callback_query.message.answer("Меню:", reply_markup=get_keyboard(["Ручной трейдинг", "Управляемый трейдинг"]))


@router.callback_query(F.data == "agree_lose")
async def agree_lose_handler(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer("Меню:", reply_markup=get_keyboard(["Ручной трейдинг", "Управляемый трейдинг"]))


@router.message(F.text == "Назад в Меню")
async def go_to_menu(callback_query: CallbackQuery):
    await callback_query.message.answer("Меню:", reply_markup=get_keyboard(["Ручной трейдинг", "Управляемый трейдинг"]))


@router.message()
async def message_handler(message: Message):
    user = await User.get_or_none(user_id=message.from_user.id)
    if user:
        if user.state == 1:
            user.state = 2
            user.trader_id = message.text.strip()
            await user.save()
            await message.answer(config.FTM)
            await asyncio.sleep(3)
            await message.answer("Меню:", reply_markup=get_keyboard(["Ручной трейдинг", "Управляемый трейдинг"]))
        if user.state == 2:
            menu = get_keyboard(["Ручной трейдинг", "Управляемый трейдинг"])
            await message.answer("Меню:", reply_markup=menu)