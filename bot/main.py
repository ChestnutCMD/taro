import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import ContentType
import asyncio
import logging

from database.models import async_main
from handlers.basic import get_balance, register_user, random_cart, prediction
from handlers.payment import order, pre_checkout, successful_payment
from utils.commands import set_commands


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(436774216, 'Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(436774216, 'Бот остановлен')


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s - '
                        '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    await async_main()
    bot = Bot(os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.message.register(register_user, Command(commands='start'))
    dp.message.register(register_user, F.text == 'Старт')
    dp.message.register(random_cart, Command(commands='cart_of_day'))
    dp.message.register(random_cart, F.text == 'Карта дня')
    dp.message.register(get_balance, Command(commands='balance'))
    dp.message.register(get_balance, F.text == 'Проверить баланс')
    dp.message.register(order, Command(commands='buy_tokens'))
    dp.message.register(order, F.text == 'Пополнить баланс')
    dp.callback_query.register(order, F.data == 'buy_tokens')
    dp.pre_checkout_query.register(pre_checkout)
    dp.message.register(successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    dp.shutdown.register(stop_bot)
    dp.message.register(prediction)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt as e:
        print(e)

