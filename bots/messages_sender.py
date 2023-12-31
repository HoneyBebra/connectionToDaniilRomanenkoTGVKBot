import requests
import random
import vk_api
import os
import json

from bots import tg_bot, vk, vk_upload


class Message:
    def __init__(self, message: str, sticker=None):
        self.message = message
        self.sticker = sticker

        self.attachment = None


class VKMessage(Message):
    async def _upload_static_sticker_on_server(self, file_path) -> None:
        sticker_file = await tg_bot.download_file(file_path)
        photo = vk_upload.photo_messages(photos=sticker_file)[0]
        self.attachment = f"photo{photo['owner_id']}_{photo['id']}"

    async def _upload_animated_sticker_on_server(self, file_path) -> None:
        # TODO: convert to .gif or .mp4
        file_url = f'https://api.telegram.org/file/bot{os.getenv("TG_TOKEN")}/{file_path}'
        file = {'file': ('animated_sticker.webm', requests.get(file_url).content)}
        upload_url = vk.docs.getMessagesUploadServer(peer_id=os.getenv('PASHA_SERYI_VK_ID'))['upload_url']
        response = requests.post(upload_url, files=file)
        result = json.loads(response.text)
        saved_file = vk.docs.save(file=result['file'], title='animated_sticker.webm')
        self.attachment = 'doc{}_{}'.format(saved_file['doc']['owner_id'], saved_file['doc']['id'])

    async def send(self) -> None:
        if self.sticker is not None:
            file = await tg_bot.get_file(self.sticker.file_id)
            file_path = file.file_path
            try:
                await self._upload_static_sticker_on_server(file_path)
            except vk_api.ApiError:
                await self._upload_animated_sticker_on_server(file_path)

        vk.messages.send(
            user_id=os.getenv('PASHA_SERYI_VK_ID'),
            random_id=random.randint(0, 999999999),
            message=self.message,
            attachment=self.attachment
        )


class TGMessage(Message):
    async def send(self) -> None:
        await tg_bot.send_message(
            os.getenv('PASHA_SERYI_TG_ID'),
            self.message
        )
