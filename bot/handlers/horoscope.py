from aiogram.types import Message, CallbackQuery

from keyboards.inline import get_zodiac_keyboard, inline_horo_markup
from utils.utils import get_text_horoscope


async def get_zodiac(message: Message):
    await message.answer('Выберите знак зодиака', reply_markup=get_zodiac_keyboard())


async def get_horoscope(call: CallbackQuery):
    await call.answer()
    zodiac = call.data
    text = await get_text_horoscope(zodiac=zodiac)
    await call.message.edit_text(text=text, reply_markup=inline_horo_markup)
