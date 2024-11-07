from typing import Union

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_keyboard(names: Union[str, list], adjust: int = 2):
    if type(names) == str:
        names = [names]
    builder = ReplyKeyboardBuilder()
    for name in names:
        builder.button(text=name)
    builder.adjust(adjust)
    return builder.as_markup()


def get_inline_keyboard(
    names: Union[str, list], adjust: int = 2, pre: str = "", custom: list = []
):
    if type(names) == str:
        names = [names]
    builder = InlineKeyboardBuilder()
    for zi, name in enumerate(names):
        data = name
        if custom:
            try:
                data = custom[zi]
            except:
                ...
        if pre:
            data = pre + "_" + name
        builder.button(text=name, callback_data=data)
    builder.adjust(adjust)
    return builder.as_markup()
