from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_admin_menu():
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="First Message"),
                KeyboardButton(text="Push Message")  
            ]
        ],
        resize_keyboard=True
    )
    return buttons