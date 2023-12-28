from vk_api.longpoll import VkLongPoll, VkEventType
import asyncio

from messages_sender import send_message_to_tg
from bots import vk_session


async def listen():
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            await send_message_to_tg(message=event.text)


if __name__ == '__main__':
    asyncio.run(listen())
