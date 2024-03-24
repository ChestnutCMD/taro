from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Старт'),
        KeyboardButton(text='Карта дня'),
        KeyboardButton(text='Помощь'),
    ],
    [
        KeyboardButton(text='Проверить баланс'),
        KeyboardButton(text='Пополнить баланс')
    ]
], resize_keyboard=True)
