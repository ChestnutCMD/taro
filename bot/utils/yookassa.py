import os

import yookassa
from yookassa import Configuration, Payment
import uuid

Configuration.account_id = os.getenv('PAYMENT_SHOP_ID')
Configuration.secret_key = os.getenv('PAYMENT_TOKEN')


def create(amount, chat_id):
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
            'return_url': 'https://t.me/tod_god_bot'
        },
        'capture': True,
        'metadata': {
            'chat_id': chat_id
        },
        'description': 'Описание товара....'
    }, id_key)

    return payment.confirmation.confirmation_url, payment.id


def check(payment_id):
    payment = yookassa.Payment.find_one(payment_id)
    if payment.status == 'succeeded':
        return payment
    else:
        return False
