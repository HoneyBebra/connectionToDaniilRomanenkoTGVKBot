from aiogram import types
import asyncio

from messages_sender import VKMessage
from bots import dp, bot


@dp.message()
async def echo_handler(message: types.Message) -> None:
    if message.sticker is not None:
        pass

    vk_message = VKMessage(message=message.text)
    await vk_message.send()


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
