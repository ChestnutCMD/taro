import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import ContentType, Update
from aiohttp import web
import asyncio
import logging

from database.models import async_main
from handlers.basic import get_balance, register_user, random_cart, prediction, buy_token, start_bot
from handlers.payment import order, pre_checkout, successful_payment


# webhook settings
WEBHOOK_HOST = f'https://tarobot.space'
WEBHOOK_PATH = f'/webhook/{os.getenv("BOT_TOKEN")}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = '7500'


async def webhook_handler(request):
    if request.match_info.get("token") == os.getenv("BOT_TOKEN"):
        data = await request.json()
        update = Update(**data)
        await dp.update(update)
        return web.Response(text="ok")
    return web.Response(text="invalid token", status=403)


app = web.Application()
app.add_routes([web.post(WEBHOOK_PATH, webhook_handler)])
bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher()


async def stop_bot():
    await bot.send_message(436774216, 'Бот остановлен')
    await bot.delete_webhook()


async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s - '
                        '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    await async_main()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
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
    dp.shutdown.register(stop_bot)
    dp.message.register(prediction)


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt as e:
        print(e)
    web.run_app(app, host="0.0.0.0", port=7500)
