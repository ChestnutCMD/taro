from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пополнить баланс', callback_data='buy_tokens')]
])
