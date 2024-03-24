from aiogram import Bot
from aiogram.types import Message, FSInputFile, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import User, Cart
from database.requests import add_user, get_user, get_carts, debiting_token, get_user_email, add_user_email
from keyboards.reply import reply_keyboard
from keyboards.inline import inline_markup
from utils.gpt import request_gpt
from utils.utils import choice_cart, choice_tree_carts, image_join
from utils.yookassa import create


async def register_user(message: Message):
    """ Регистрация пользователя """
    telegram_id: int = message.from_user.id
    first_name: str = message.from_user.first_name
    user: User = await get_user(telegram_id)
    if user is None:
        await add_user(first_name, telegram_id)
    await message.answer(text=f'Добро пожаловать, {first_name}!', reply_markup=reply_keyboard)
    await message.delete()


async def add_email(message: Message):
    """ Добавление почты пользователя """
    await add_user_email(message.from_user.id, message.text)
    await message.answer('Ваша почта добавлена. Теперь можете перейти к оплате')


async def get_balance(message: Message):
    """ Проверить баланс """
    user_id: int = message.from_user.id
    user: User = await get_user(user_id)
    await message.answer(f'Ваш баланс: {user.token} token', reply_markup=inline_markup)
    await message.delete()


async def buy_token(message: Message | CallbackQuery):
    """ Покупка токенов """
    email = await get_user_email(message.from_user.id)
    if email is None:
        await message.answer('Введите свой Email. Это необходимо для отправки чеков о покупке')
    else:
        if isinstance(message, Message):
            user: User = await get_user(message.chat.id)
            url_100 = create(amount='100.00', message=message, user=user)
            url_200 = create(amount='200.00', message=message, user=user)
            url_500 = create(amount='500.00', message=message, user=user)

            builder = InlineKeyboardBuilder()
            builder.add(InlineKeyboardButton(
                text='10 токенов',
                url=url_100
            ))
            builder.add(InlineKeyboardButton(
                text='20 токенов',
                url=url_200
            ))
            builder.add(InlineKeyboardButton(
                text='10 токенов',
                url=url_500
            ))
            await message.answer('Выберите колличество', reply_markup=builder.as_markup())

        elif isinstance(message, CallbackQuery):
            call = message
            user: User = await get_user(call.message.chat.id)
            url_100 = create(amount='100.00', message=call, user=user)
            url_200 = create(amount='200.00', message=call, user=user)
            url_500 = create(amount='500.00', message=call, user=user)

            builder = InlineKeyboardBuilder()
            builder.add(InlineKeyboardButton(
                text='10 токенов',
                url=url_100
            ))
            builder.add(InlineKeyboardButton(
                text='20 токенов',
                url=url_200
            ))
            builder.add(InlineKeyboardButton(
                text='10 токенов',
                url=url_500
            ))
            await call.message.answer('Выберите колличество', reply_markup=builder.as_markup())


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


async def bot_help(message: Message):
    """ Помощь """
    await message.answer('Список доступных команд:\n'
                         '/start - начало работы с ботом \n'
                         '/cart_of_day - Карта дня. Получение одной карты и объяснения ее значения.\n'
                         '/help - Помощь. Вывод всех доступных команд.\n'
                         '/balance - Проверить баланс.\n'
                         '/buy_tokens - Покупка токенов. Для покупки необходимо добавить свой email адрес '
                         '(это необходимо для отправки чека о покупке). '
                         'Для этого просто напишите в чат свой email адрес. '
                         'Выберите колличество токенов, которое хотите купить.\n'                         
                         'Моя главная функция - это ответы на ваши впоросы на основе карт таро '
                         'Для этого напишите в чат вопрос, который вас интересует, '
                         'и я сделаю предсказание на основе выпавших карт таро. '
                         'За один вопрос списывается 1 токен (1 токен = 10 руб). Изначально вам доступно 5 токенов'
                         )
