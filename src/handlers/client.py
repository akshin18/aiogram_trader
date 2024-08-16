import asyncio
import datetime
import os
import random

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from loguru import logger

from config_reader import config, TRADER_TOOLS, time_splitter, lose_text, google_sheet
from filters.filter import TraderFilter
from utils import language
from utils.func import is_auto_trade, req_user, send_indicator
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


@router.message(F.text == language.manual_trading[config.LANG])
async def manual_trading_handler(message: Message):
    user = await User.get_or_none(user_id=message.from_user.id)
    user.manual_click_count += 1
    await user.save()
    google_sheet.update_manual_trading(user.user_id, user.manual_click_count)
    if user:
        if user.state == 3:
            return
        if not user.is_paid:
            user.top_up_date = datetime.datetime.now(google_sheet.moscow_timezone).strftime("%d/%m/%Y, %H:%M:%S")
            await user.save()
            google_sheet.update_top_up(user.user_id, user.top_up_date)
            await message.answer(language.for_pay[config.LANG])
            return
        await message.answer(
            language.options[config.LANG], reply_markup=get_inline_keyboard(list(TRADER_TOOLS.keys()))
        )


@router.callback_query(F.data.in_(list(TRADER_TOOLS.keys())))
async def trading_type_callback(callback_query: CallbackQuery):
    await callback_query.message.delete()
    user = await User.get_or_none(user_id=callback_query.from_user.id)
    site = callback_query.data
    if (
        user.trade_type == site
        and user.trade_choose_time is not None
        and user.trade_choose_time > datetime.datetime.now(datetime.UTC)
    ):
        random_trader_tools = user.trade_tools.split("&&")
    else:
        logger.debug(user.trade_choose_time)
        user.trade_type = site
        user.trade_choose_time = datetime.datetime.now(
            datetime.UTC
        ) + datetime.timedelta(seconds=10 * 60)
        random_trader_tools = random.choices(TRADER_TOOLS[site]["tools"], k=5)
        user.trade_tools = "&&".join(random_trader_tools)
    await user.save()
    await callback_query.message.answer(
        language.analise_found_5[config.LANG],
        reply_markup=get_inline_keyboard(random_trader_tools, pre="tradingtype"),
    )


@router.callback_query(F.data.startswith("tradingtype_"))
async def trade_tools_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    user = await User.get_or_none(user_id=callback_query.from_user.id)
    if user:
        trade_time = TRADER_TOOLS[user.trade_type]["time"]
        trade_choose_tools = callback_query.data.split("_", maxsplit=1)[1]
        user.trade_choose_tools = trade_choose_tools
        await user.save()
        if not trade_time and user.state == 2:
            await send_indicator(callback_query.message, user, trade_choose_tools, 15)
            return
        await state.set_data({"tools": trade_choose_tools})
        trade_image = TRADER_TOOLS[user.trade_type].get("image")
        if trade_image:
            await callback_query.message.answer_photo(trade_image)
        await callback_query.message.answer(
            language.options[config.LANG], reply_markup=get_inline_keyboard(trade_time, pre="tradetime")
        )


@router.callback_query(F.data.startswith("tradetime_"))
async def trade_time_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    user = await User.get_or_none(user_id=callback_query.from_user.id)
    if user and user.state == 2:
        time_str = callback_query.data.split("_", maxsplit=1)[1]
        trade_time = time_splitter.get(time_str, 15)
        user.trade_time = time_str
        data = await state.get_data()
        trade_choose_tools = data["tools"]
        user.trade_choose_tools = trade_choose_tools
        await user.save()
        await send_indicator(
            callback_query.message,
            user,
            trade_choose_tools,
            trade_time,
            callback_query.data.split("_", maxsplit=1)[1],
        )


@router.message(F.text == language.auto_trading[config.LANG])
async def manual_trading_handler(message: Message):
    user = await User.get_or_none(user_id=message.from_user.id)
    if user:
        user.trade_mode = 1
        user.auto_click_count += 1
        await user.save()
        google_sheet.update_auto_trading(user.user_id, user.auto_click_count)
        inline_keyboard = get_inline_keyboard(language.auto_trading_signals_time[config.LANG], custom=["auto_time_2", "auto_time_4", "auto_time_5"])
        await message.answer(
            language.auto_trading_question_count[config.LANG],
            reply_markup=inline_keyboard
        )


@router.callback_query(F.data == language.win[config.LANG])
async def win_handler(callback_query: CallbackQuery, state: FSMContext):
    user = await User.get_or_none(user_id=callback_query.from_user.id)
    if user and user.state == 4:
        await callback_query.message.delete()
        await state.set_state(WinState.win)
        await callback_query.message.answer(language.win_amount[config.LANG])


@router.message(WinState.win)
async def win_count_handler(message: Message, state: FSMContext):
    user = await User.get_or_none(user_id=message.from_user.id)
    user.state = 2
    user.win_count += 1
    await user.save()
    google_sheet.update_win_count(user.user_id, user.win_count)
    await state.clear()
    if user:
        if not await is_auto_trade(user, message, result="win"):
            await message.answer(
                language.menu[config.LANG],
                reply_markup=get_keyboard(language.trading_methods[config.LANG]),
            )


@router.callback_query(F.data == language.lose[config.LANG])
async def win_handler(callback_query: CallbackQuery):
    await callback_query.message.delete()
    user = await User.get_or_none(user_id=callback_query.from_user.id)
    if user and user.state == 4:
        user.state = 2
        user.last_lose_count += 1
        google_sheet.update_lose_win_count(user.user_id, user.win_count - user.last_lose_count)
        if not await is_auto_trade(user, callback_query.message, result="lose"):
            if user.lose_count >= 2:
                await callback_query.message.answer(
                    lose_text,
                    reply_markup=get_inline_keyboard(
                        language.lose_confirm_refresh[config.LANG],
                        custom=["agree_lose"],
                    ),
                )
                user.lose_count = 0
            else:
                user.lose_count += 1
                await callback_query.message.answer(
                    language.menu[config.LANG],
                    reply_markup=get_keyboard(language.trading_methods[config.LANG]),
                )
        await user.save()


@router.callback_query(F.data == "agree_lose")
async def agree_lose_handler(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        language.menu[config.LANG], reply_markup=get_keyboard(language.trading_methods[config.LANG])
    )


@router.message(F.text == language.back[config.LANG])
async def go_to_menu(callback_query: CallbackQuery):
    await callback_query.message.answer(
        language.menu[config.LANG], reply_markup=get_keyboard(language.trading_methods[config.LANG])
    )


@router.message()
async def message_handler(message: Message, state: FSMContext):
    user = await User.get_or_none(user_id=message.from_user.id)
    if user:
        if user.state == 1:
            user.state = 2
            user.trader_id = message.text.strip()
            await user.save()
            await message.answer(language.ftm[config.LANG])
            await asyncio.sleep(3)
            await message.answer(
                language.menu[config.LANG],
                reply_markup=get_keyboard(language.trading_methods[config.LANG]),
            )
        if user.state == 2:
            menu = get_keyboard(language.trading_methods[config.LANG])
            await message.answer(language.menu[config.LANG], reply_markup=menu)


@router.callback_query(F.data.in_(["auto_time_2", "auto_time_4", "auto_time_5"]))
async def handle_trader_time_auto(callback_query: CallbackQuery):
    await callback_query.message.delete()
    user = await User.get_or_none(user_id=callback_query.from_user.id)
    if user:
        auto_trade_count = callback_query.data.split("auto_time_")[-1]
        random_trade_type = random.choice(list(TRADER_TOOLS.keys()))
        random_trade_tool = random.choice(TRADER_TOOLS[random_trade_type]['tools'])
        trade_time = TRADER_TOOLS[random_trade_type].get('time')
        random_time = random.randint(2,6)
        if trade_time and len(trade_time) > 3:
            random_trade_time_str = trade_time[-3].replace("5", str(random_time))
        else:
            random_trade_time_str = language.default_seconds[config.LANG]
        
        if auto_trade_count == "2":
            auto_trade_left_time = 10 - random_time
        elif auto_trade_count == "4":
            auto_trade_left_time = 20 - random_time
        else:
            auto_trade_left_time = 30 - random_time
        
        user.trade_type = random_trade_type
        user.trade_tools = random_trade_tool
        user.trade_time = random_trade_time_str
        user.auto_trade_choose_count = int(auto_trade_count)
        user.auto_trade_count = 1
        user.trade_mode = 1
        user.auto_trade_time_left = auto_trade_left_time
        await user.save()
        text = language.choose_trade_pair[config.LANG].format(random_trade_tool=random_trade_tool, random_trade_type=random_trade_type, random_trade_time_str=random_trade_time_str)
        inline_keyboard = get_inline_keyboard(language.confirm_choice[config.LANG], custom=["agree_auto_trade"])
        await callback_query.message.answer(text, reply_markup=inline_keyboard)


@router.callback_query(F.data == "agree_auto_trade")
async def handle_trader_agree_auto(callback_query: CallbackQuery):
    await callback_query.message.delete()
    user = await User.get_or_none(user_id=callback_query.from_user.id)
    print(user)
    print(user.state)
    if user:
        trade_time = time_splitter[user.trade_time]
        if user.state == 2:
            await send_indicator(callback_query.message, user, user.trade_choose_tools, trade_time, user.trade_time)
        
        
@router.callback_query(F.data == "i_have_refreshed_site")
async def handle_trader_agree_auto(callback_query: CallbackQuery):
    await callback_query.message.delete()