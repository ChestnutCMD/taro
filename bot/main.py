import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import ContentType
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import logging

from database.models import async_main
from handlers.basic import get_balance, register_user, random_cart, prediction, buy_token
from handlers.payment import order, pre_checkout, successful_payment
from utils.commands import set_commands

# webhook settings
WEBHOOK_PATH = f'/webhook/{os.getenv("BOT_TOKEN")}'
WEBHOOK_URL = f'https://tarobot.space{WEBHOOK_PATH}'
WEBHOOK_SECRET = 'secret'


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
    await bot.send_message(436774216, 'Бот запущен')


async def stop_bot(bot: Bot):
    await bot.delete_webhook()


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s - '
                        '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.message.register(register_user, Command(commands='start'))
    dp.message.register(register_user, F.text == 'Старт')
    dp.message.register(random_cart, Command(commands='cart_of_day'))
    dp.message.register(random_cart, F.text == 'Карта дня')
    dp.message.register(get_balance, Command(commands='balance'))
    dp.message.register(get_balance, F.text == 'Проверить баланс')
    dp.message.register(buy_token, Command(commands='buy_tokens'))
    dp.message.register(buy_token, F.text == 'Пополнить баланс')
    dp.callback_query.register(buy_token, F.data == 'buy_tokens')
    dp.callback_query.register(order)
    dp.pre_checkout_query.register(pre_checkout)
    dp.message.register(successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    dp.message.register(prediction)
    dp.shutdown.register(stop_bot)
    bot = Bot(os.getenv('BOT_TOKEN'))
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host='0.0.0.0', port=7500)


if __name__ == '__main__':
    asyncio.run(async_main())
    main()
