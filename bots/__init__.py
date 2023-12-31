import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import vk_api
from vk_api import VkUpload


load_dotenv()

dp = Dispatcher()
tg_bot = Bot(os.getenv('TG_TOKEN'))

vk_session = vk_api.VkApi(token=os.getenv('VK_TOKEN'))
vk = vk_session.get_api()
vk_upload = VkUpload(vk_session)
