import os

import yookassa
from aiogram.types import CallbackQuery
from yookassa import Configuration, Payment
import uuid

from database.models import User

Configuration.account_id = os.getenv('PAYMENT_SHOP_ID')
Configuration.secret_key = os.getenv('PAYMENT_TOKEN')


def create(amount: str, call: CallbackQuery, user: User):
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
            'chat_id': call.message.chat.id
        },
        'description': 'Покупка токенов',
        "receipt": {
            "customer": {
                "full_name": user.name,
                "email": user.email,
                "phone": "79297579477"
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

    return payment.confirmation.confirmation_url, payment.id


def check(payment_id):
    payment = yookassa.Payment.find_one(payment_id)
    if payment.status == 'succeeded':
        return payment
    else:
        return False
