import os
from aiogram.types import CallbackQuery, Message
from yookassa import Configuration, Payment
import uuid

from database.models import User
from database.requests import get_user, add_token, add_transaction

Configuration.account_id = os.getenv('PAYMENT_SHOP_ID')
Configuration.secret_key = os.getenv('PAYMENT_TOKEN')


def create(amount: str, message: Message | CallbackQuery, user: User):
    if isinstance(message, Message):
        chat_id = message.chat.id
    else:
        chat_id = message.message.chat.id
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            'value': amount,
            'currency': "RUB"
        },
        'paymnet_method_data': {
            'type': 'bank_card'
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': 'https://t.me/Taro_tarobot'
        },
        'capture': True,
        'metadata': {
            'chat_id': chat_id
        },
        'description': 'Покупка токенов',
        "receipt": {
            "customer": {
                "full_name": user.name,
                "email": user.email,
            },
            "items": [
                {
                    "description": f"Покупка {float(amount)/10} токенов",
                    "quantity": "1.00",
                    "amount": {
                        "value": amount,
                        "currency": "RUB"
                    },
                    "vat_code": "2",
                    "payment_mode": "full_payment",
                    "payment_subject": "payment",
                    "supplier": {
                        "name": "Леонтьева Ильвина",
                        "phone": "+7 929 753-58-15",
                        "inn": "023400437033"
                    }
                },
            ]
        }
    }, id_key)

    return payment.confirmation.confirmation_url


async def check_payment(telegram_id, price, currency):
    user = await get_user(telegram_id)
    await add_token(telegram_id, int(price / 10))
    await add_transaction(user_id=user.id, currency=currency, price=price)
