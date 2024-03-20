from aiogram import Bot
from aiogram.types import Message, FSInputFile, CallbackQuery

from database.models import User, Cart
from database.requests import add_user, get_user, get_carts, debiting_token
from keyboards.reply import reply_keyboard
from keyboards.inline import inline_markup, inline_markup_payment
from utils.gpt import request_gpt
from utils.utils import choice_cart, choice_tree_carts, image_join


async def register_user(message: Message):
    """ Регистрация пользователя """
    telegram_id: int = message.from_user.id
    first_name: str = message.from_user.first_name
    user: User = await get_user(telegram_id)
    if user is None:
        await add_user(first_name, telegram_id)
    await message.answer(text=f'Добро пожаловать, {first_name}!', reply_markup=reply_keyboard)
    await message.delete()


async def get_balance(message: Message):
    """ Проверить баланс """
    user_id: int = message.from_user.id
    user: User = await get_user(user_id)
    await message.answer(f'Ваш баланс: {user.token} token', reply_markup=inline_markup)
    await message.delete()


async def buy_token(message: Message | CallbackQuery):
    """ Покупка токенов """
    if isinstance(message, Message):
        await message.answer('Выберите колличество', reply_markup=inline_markup_payment)
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.answer('Выберите колличество', reply_markup=inline_markup_payment)


async def random_cart(message: Message, bot: Bot):
    """ Карта дня. Выбирает случайную карту"""
    cart_id: int = choice_cart()
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(f'./Images/Carts/{cart_id}.jpg'))
    cart = await get_carts(cart_id)
    await message.answer(f'{cart.name}\n{cart.description}')
    await message.delete()


async def prediction(message: Message, bot: Bot):
    """ Выбирает случайные 3 карты """
    chat_id: int = message.chat.id
    carts = choice_tree_carts()
    user = await get_user(chat_id)
    if user.token > 0:
        photo_1 = f'./Images/Carts/{carts[0]}.jpg'
        photo_2 = f'./Images/Carts/{carts[1]}.jpg'
        photo_3 = f'./Images/Carts/{carts[2]}.jpg'
        image = image_join(photo_1, photo_2, photo_3, name=str(chat_id))
        await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(image))

        cart_1: Cart = await get_carts(carts[0])
        cart_2: Cart = await get_carts(carts[1])
        cart_3: Cart = await get_carts(carts[2])
        predict = request_gpt(message.text, cart_1.name, cart_2.name, cart_3.name)
        await message.answer(f'{cart_1.name}, {cart_2.name}, {cart_3.name}.\n{predict}')
        await debiting_token(chat_id)
    else:
        await message.answer('Недостаточный баланс', reply_markup=inline_markup)
