import os

from aiogram import Bot
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery

from database.requests import add_token, get_user, add_transaction


async def order(call: CallbackQuery, bot: Bot):
    if call.data == '5':
        price = 5000
    elif call.data == '10':
        price = 10000
    elif call.data == '20':
        price = 20000
    else:
        price = 50000

    await bot.send_invoice(chat_id=call.message.chat.id,
                           title='Пополнение баланса',
                           description=f'Купить {call.data} токенов',
                           payload='invoice',
                           provider_token=os.getenv('PAYMENT_TOKEN'),
                           currency='RUB',
                           prices=[LabeledPrice(label='Покупка токенов',
                                                amount=price)],
                           start_parameter='taro',
                           photo_url='blob:https://web.telegram.org/36eb4643-d58e-4d99-9faf-71e884639c2a',
                           photo_size=200,
                           photo_height=350,
                           photo_width=362,
                           need_name=False,
                           need_phone_number=False,
                           need_email=False,
                           need_shipping_address=False,
                           is_flexible=False,
                           disable_notification=False,
                           reply_markup=None,
                           reply_to_message_id=None)


async def pre_checkout(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: Message):
    chat_id: int = message.chat.id
    user = await get_user(chat_id)
    user_id = user.id
    currency = message.successful_payment.currency
    price = message.successful_payment.total_amount/100
    await add_token(chat_id, int(price/10))
    await message.answer(f'Ваш баланс пополнен на {price/1000} токенов')
    await add_transaction(user_id=user_id, currency=currency, price=price)
