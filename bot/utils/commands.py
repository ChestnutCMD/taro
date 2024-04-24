from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='cart_of_day',
            description='Карта дня'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='balance',
            description='Проверить баланс'
        ),
        BotCommand(
            command='buy_tokens',
            description='Покупка токенов'
        )
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
