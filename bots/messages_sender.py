import os
import random

from bots import bot, vk


async def send_message_to_tg(message: str):
    await bot.send_message(
        os.getenv('PASHA_SERYI_TG_ID'), message
    )


async def send_message_to_vk(message: str):
    vk.messages.send(
        user_id=os.getenv('PASHA_SERYI_VK_ID'),
        random_id=random.randint(0, 999999999),
        message=message
    )
