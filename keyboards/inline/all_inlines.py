from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.tests import test_uz


langs = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru")
        ]
    ]
)

start_test_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Unda testimizga marhamat🚀", callback_data="start_test_uz")
        ]
    ]
)

application = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Sinov darsiga yozilish", callback_data='application')
        ]
    ]
)

filials = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Yunusobod📍", callback_data='yunusobod')
        ],
        [
            InlineKeyboardButton("Tinchlik📍", callback_data='tinchlik')
        ],
        [
            InlineKeyboardButton("Chilonzor - Qutbiniso📍", callback_data='chilonzor')
        ],
        [
            InlineKeyboardButton("Sergeli📍", callback_data='sergeli')
        ]
    ]
)

    