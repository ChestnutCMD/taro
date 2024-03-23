import asyncio
import os

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import logging

from database.models import async_main
from handlers.basic import get_balance, register_user, random_cart, prediction, buy_token, add_email, bot_help
from handlers.yookassa_handlers import buy_handler, check_payment
from utils.commands import set_commands

# webhook settings
WEBHOOK_PATH = f'/webhook/{os.getenv("BOT_TOKEN")}'
WEBHOOK_URL = f'https://tarobot.space{WEBHOOK_PATH}'
WEBHOOK_SECRET = 'secret'

bot = Bot(os.getenv('BOT_TOKEN'))


async def handle_post_request(request):
    data = await request.json()

    price = data['object']['amount']['value']
    currency = data['object']['amount']['currency']
    telegram_id = int(data['object']['metadata']['chat_id'])

    if data['object']['status'] == 'succeeded':
        await check_payment(telegram_id, price, currency)
        await bot.send_message(chat_id=telegram_id, text=f'Ваш баланс пополнен на {price / 10} токенов')
    else:
        await bot.send_message(chat_id=telegram_id, text=f'Что-то пошло не так')
    return aiohttp.web.Response(text="ok", status=200)


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)
    await bot.send_message(436774216, 'Бот запущен')


async def stop_bot(bot: Bot):
    await bot.delete_webhook()


def main(bot: Bot):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s - '
                        '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.message.register(register_user, Command(commands='start'))
    dp.message.register(register_user, F.text == 'Старт')
    dp.message.register(bot_help, Command(commands='help'))
    dp.message.register(bot_help, F.text == 'Помощь')
    dp.message.register(random_cart, Command(commands='cart_of_day'))
    dp.message.register(random_cart, F.text == 'Карта дня')
    dp.message.register(get_balance, Command(commands='balance'))
    dp.message.register(get_balance, F.text == 'Проверить баланс')
    dp.message.register(buy_token, Command(commands='buy_tokens'))
    dp.message.register(buy_token, F.text == 'Пополнить баланс')
    dp.callback_query.register(buy_token, F.data == 'buy_tokens')
    dp.callback_query.register(buy_handler)
    dp.message.register(add_email, F.text.regexp(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'))
    dp.message.register(prediction)
    dp.shutdown.register(stop_bot)
    app = web.Application()
    app.router.add_post('/payment', handle_post_request)  # роут для обработки платежей
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=WEBHOOK_SECRET)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host='0.0.0.0', port=7500)


if __name__ == '__main__':
    asyncio.run(async_main())
    main(bot)
