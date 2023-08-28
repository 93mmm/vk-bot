from vk_api import VkApi
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod

from helpers import get_photo_url
from structs import ConversationCaches
from message import Voice, Doc, Photo
from const import STICKER, VOICE_MESSAGE, TEXT_MESSAGE, NOT_FOUND


class ReceivedMessage:
    def __init__(self, vk: VkApi, event: Event):
        self.api: VkApiMethod = vk.get_api()

        self.cache: ConversationCaches = ConversationCaches()

        self.conversation_id: int = None
        self.conversation_name: str = None
        self.sticker_id: int = None

        self.attachments: list[Voice | Doc | Photo] = None
        self.message_text: str = None
        self.time: int = None

        self.is_it_voice_message: str = False

        self.message_id = event.message_id
        self.conversation_id = event.peer_id
        self.conversation_name = self._get_sender_name(event)
        self.sticker_id = self._get_sticker(event.attachments)

        self.attachments = self._get_attachments(event.attachments)
        self.message_text = event.message
        self.time = event.datetime

    def _get_sender_name(self, event: Event) -> str:
        name = self.cache.get_name(event.peer_id)
        if name == NOT_FOUND:
            if event.from_user:
                usr = self.api.users.get(user_ids=str(self.conversation_id))[0]
                return f"{usr['first_name']} {usr['last_name']}"
            elif event.from_chat:
                return (
                    self.api.messages.getConversationsById(peer_ids=self.conversation_id,
                                                        extended=1,
                                                        fields="chat_settings")
                )["items"][0]["chat_settings"]["title"]
            elif event.from_group:
                return self.api.groups.getById(group_id=abs(self.conversation_id))[0]["name"]
        return name

    def _get_attachments(self, attachments: dict) -> list[Voice | Doc | Photo]:
        list_of_attachments: list[Voice | Doc | Photo] = list()
        rsp = self.api.messages.getById(message_ids=self.message_id)["items"][0]["attachments"]
        for el in rsp:
            if el["type"] == "photo":
                received_photo = el["photo"]
                url = get_photo_url(received_photo["sizes"])
                if "png" in url:
                    ext = "png"
                elif "jpg" in url or "jpeg":
                    ext = "jpg"
                else:
                    ext = "gif"
                path = f"photo{received_photo['owner_id']}_{received_photo['id']}.{ext}"
                photo = Photo()
                photo.prepare_to_download(path, url)
                list_of_attachments.append(photo)
            elif el["type"] == "doc":
                doc = Doc()
                doc.prepare_to_download(el["doc"]["title"], el["doc"]["url"])
                list_of_attachments.append(doc)
            elif el["type"] == "audio_message":
                vm = Voice()
                path = f"audio_message{el['audio_message']['owner_id']}_{el['audio_message']['id']}.ogg"
                vm.prepare_to_download(path, el["audio_message"]["link_ogg"])
                list_of_attachments.append(vm)
        return list_of_attachments

    def _get_sticker(self, attachments: dict) -> int:
        if "attach1_type" in attachments and attachments["attach1_type"] == "sticker":
            return attachments["attach1"]
        return 0

    def get_type(self):
        if self.sticker_id != 0:
            return STICKER
        if len(self.attachments) > 0 and type(self.attachments[0]) == Voice:
            return VOICE_MESSAGE
        return TEXT_MESSAGE
    
    def download_attachments(self):
        for el in self.attachments:
            el.download()

    def __str__(self):
        output = list()
        if self.message_text:
            output.append(f"Text: {self.message_text}")
        if self.sticker_id != 0:
            output.append(f"Sticker: {self.sticker_id}")

        output.append(f"From: {self.conversation_id} ({self.conversation_name})")
        atts = "Attachments"
        if self.is_it_voice_message:
            atts = "Voice message"
        if len(self.attachments) != 0:
            attachments = " | ".join(list(map(str, self.attachments)))
            output.append(f"{atts}: {attachments}")
        output.append(f"At the time: {self.time}\n\n")

        return "\n".join(output)
