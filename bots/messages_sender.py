import requests
import random
import os
import json

from bots import tg_bot, vk, vk_upload


class Message:
    def __init__(
            self, message: str, sticker=None,
            voice=None, photo=None, video_circle=None
    ):
        self.message = message
        self.sticker = sticker
        self.voice = voice
        self.photo = photo
        self.video_circle = video_circle

        self.attachment = None


class VKMessage(Message):
    async def _upload_photo_on_server(self, sticker_file_path) -> None:
        sticker_file = await tg_bot.download_file(sticker_file_path)
        photo = vk_upload.photo_messages(photos=sticker_file)[0]
        self.attachment = f"photo{photo['owner_id']}_{photo['id']}"

    async def _upload_video_sticker_on_server(self, sticker_file_path) -> None:
        # TODO: convert to .gif or .mp4
        file_url = f'https://api.telegram.org/file/bot{os.getenv("TG_TOKEN")}/{sticker_file_path}'
        file = {'file': ('video_sticker.webm', requests.get(file_url).content)}
        upload_url = vk.docs.getMessagesUploadServer(
            peer_id=os.getenv('PASHA_SERYI_VK_ID')
        )['upload_url']
        response = requests.post(upload_url, files=file)
        result = json.loads(response.text)
        saved_file = vk.docs.save(file=result['file'], title='video_sticker.webm')['doc']
        self.attachment = f"doc{saved_file['owner_id']}_{saved_file['id']}"

    async def _sticker_check(self) -> None:
        if self.sticker is not None:
            sticker_file = await tg_bot.get_file(self.sticker.file_id)
            sticker_file_path = sticker_file.file_path
            if self.sticker.is_video:
                await self._upload_video_sticker_on_server(sticker_file_path)
            elif self.sticker.is_animated:
                self.message = 'Поддержка анимированных стикеров в разработке'
            else:
                await self._upload_photo_on_server(sticker_file_path)

    async def _voice_message_check(self):
        if self.voice:
            voice_file = await tg_bot.get_file(self.voice.file_id)
            voice_file_path = voice_file.file_path
            voice = await tg_bot.download_file(voice_file_path)

            # TODO: can't send a bytes object, correct
            with open('temp_voice/voice.mp3', 'wb') as f:
                f.write(voice.getbuffer())

            voice = vk_upload.audio_message(
                'temp_voice/voice.mp3', peer_id=os.getenv('PASHA_SERYI_VK_ID')
            )['audio_message']
            self.attachment = f"audio_message{voice['owner_id']}_{voice['id']}"

    async def _photo_message_check(self):
        if self.photo:
            photo = await tg_bot.get_file(self.photo[-1].file_id)
            photo_path = photo.file_path
            await self._upload_photo_on_server(photo_path)

    async def _video_circle_check(self):
        if self.video_circle:
            circle_file = await tg_bot.get_file(self.video_circle.file_id)
            circle_file_path = circle_file.file_path
            circle = await tg_bot.download_file(circle_file_path)
            print(circle)

    async def send(self) -> None:
        await self._sticker_check()
        await self._voice_message_check()
        await self._photo_message_check()
        await self._video_circle_check()

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
