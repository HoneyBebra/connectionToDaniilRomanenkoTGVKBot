from aiogram import types
import asyncio

from messages_sender import VKMessage
from bots import dp, tg_bot


@dp.message()
async def echo_handler(message: types.Message) -> None:
    vk_message = VKMessage(
        message=message.text, sticker=message.sticker,
        voice=message.voice
    )
    await vk_message.send()


async def start_polling() -> None:
    await dp.start_polling(tg_bot)


if __name__ == "__main__":
    asyncio.run(start_polling())
