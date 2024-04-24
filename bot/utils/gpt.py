import os
from openai import OpenAI


def request_gpt(question: str, cart_1: str, cart_2: str, cart_3: str) -> str:

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f"Представь что ты гадалка и гадаешь мне на картах таро. Мой вопрос: {question}.\
               Выпали следующие карты: {cart_1}, {cart_2}, {cart_3}. \
               Тебе нужно истолковать эти карты относительно моего вопроса"

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content


def simple_gpt(question: str) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": question}]
    )
    return completion.choices[0].message.content
