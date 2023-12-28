from aiogram import types
import asyncio

from messages_sender import send_message_to_vk
from bots import dp, bot


@dp.message()
async def echo_handler(message: types.Message) -> None:
    await send_message_to_vk(message=message.text)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
