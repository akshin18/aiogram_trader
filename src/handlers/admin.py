from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from config_reader import TRADER_TOOLS, config
from utils.func import set_subscribed, set_paid
from keyboards.common import get_inline_keyboard, get_keyboard
from filters.filter import AdminFilter

router = Router()
router.message.filter(AdminFilter())

@router.message(F.text.startswith("/activate"))
async def activate_handler(message: Message):
    try:
        user_id = int(message.text.split(" ")[1])
        await set_subscribed(user_id)
        await message.answer(f"Пользователь {user_id} активирован")
        await message.bot.send_message(user_id, "Отправьте ваш ид пользователя Exnova в таком формате: 123456789")
    except:
        await message.answer("Не правильный user_id")

@router.message(F.text.startswith("/paid"))
async def paid_handler(message: Message):
    try:
        user_id = int(message.text.split(" ")[1])
        await set_paid(user_id)
        await message.answer(f"Пользователь {user_id} Заплатил")
        await message.bot.send_message(user_id, "Теперь вам активна функция трейдинга в ручном режиме что бы начать торговать нажмите кнопку опции", reply_markup=get_inline_keyboard(list(TRADER_TOOLS.keys())))
    except:
        await message.answer("Не правильный user_id")

