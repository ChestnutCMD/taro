import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class EmailFilter(BaseFilter):
    async def check(self, message: Message) -> bool:
        if message.text:
            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.match(pattern, message.text):
                return True
        return False
