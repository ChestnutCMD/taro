from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пополнить баланс', callback_data='buy_tokens')]
])

inline_markup_payment = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='10 токенов', callback_data='10'),
     InlineKeyboardButton(text='20 токенов', callback_data='20'),
     InlineKeyboardButton(text='50 токенов', callback_data='50')]
])
