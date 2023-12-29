import os
import random

from bots import bot, vk


class Message:
    def __init__(self, message: str):
        self.message = message


class VKMessage(Message):
    async def send(self) -> None:
        vk.messages.send(
            user_id=os.getenv('PASHA_SERYI_VK_ID'),
            random_id=random.randint(0, 999999999),
            message=self.message
        )


class TGMessage(Message):
    async def send(self) -> None:
        await bot.send_message(
            os.getenv('PASHA_SERYI_TG_ID'),
            self.message
        )
