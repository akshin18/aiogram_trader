from aiogram.fsm.state import StatesGroup, State


class WinState(StatesGroup):
    win = State()


class TraderId(StatesGroup):
    trade_id = State()
