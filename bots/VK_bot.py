from vk_api.longpoll import VkLongPoll, VkEventType
import asyncio

from messages_sender import TGMessage
from bots import vk_session


async def listen() -> None:
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            tg_message = TGMessage(message=event.text)
            await tg_message.send()


if __name__ == '__main__':
    asyncio.run(listen())
