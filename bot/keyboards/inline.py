from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

inline_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пополнить баланс', callback_data='buy_tokens')]
])

inline_markup_payment = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='5 токенов', callback_data='5'),
     InlineKeyboardButton(text='10 токенов', callback_data='10'),
     InlineKeyboardButton(text='20 токенов', callback_data='20'),
     InlineKeyboardButton(text='50 токенов', callback_data='50')]
])


def get_zodiac_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Овен', callback_data='aries')
    keyboard_builder.button(text='Телец', callback_data='taurus')
    keyboard_builder.button(text='Близнецы', callback_data='gemini')
    keyboard_builder.button(text='Рак', callback_data='cancer')
    keyboard_builder.button(text='Лев', callback_data='leo')
    keyboard_builder.button(text='Дева', callback_data='virgo')
    keyboard_builder.button(text='Весы', callback_data='libra')
    keyboard_builder.button(text='Скорпион', callback_data='scorpio')
    keyboard_builder.button(text='Стрелец', callback_data='sagittarius')
    keyboard_builder.button(text='Козерог', callback_data='capricorn')
    keyboard_builder.button(text='Водолей', callback_data='aquarius')
    keyboard_builder.button(text='Рыбы', callback_data='pisces')
    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()


inline_horo_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вчера', callback_data='yesterday'),
     InlineKeyboardButton(text='Сегодня', callback_data='today'),
     InlineKeyboardButton(text='Завтра', callback_data='tomorrow')],
    [InlineKeyboardButton(text='Неделя', callback_data='week'),
     InlineKeyboardButton(text='Месяц', callback_data='month'),
     InlineKeyboardButton(text='Год', callback_data='year')]
])
