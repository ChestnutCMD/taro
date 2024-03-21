from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Старт'),
        KeyboardButton(text='Карта дня'),
        KeyboardButton(text='Проверить баланс'),
        KeyboardButton(text='Гороскоп')
    ],
    [
        KeyboardButton(text='Пополнить баланс')
    ]
], resize_keyboard=True)
