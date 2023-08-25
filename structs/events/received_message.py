from vk_api import VkApi
from vk_api.longpoll import Event
from vk_api.vk_api import VkApiMethod

from structs import JsonDialogsDB
from message import Voice, Doc, Photo

class ReceivedMessage:
    STICKER = 1
    VOICE_MESSAGE = 2
    TEXT_MESSAGE = 3

    def __init__(self, vk: VkApi, event: Event):
        self.api: VkApiMethod = vk.get_api()

        self.db_holder: JsonDialogsDB = JsonDialogsDB()

        self.conversation_id: int = None
        self.conversation_name: str = None
        self.sticker_id: int = None

        self.attachments: list[Voice | Doc | Photo] = None
        self.message_text: str = None
        self.time: int = None

        self.is_it_voice_message: str = False

        self.conversation_id = event.peer_id
        self.conversation_name = self._get_sender_name(event)
        self.sticker_id = self._get_sticker(event.attachments)

        self.attachments = self._get_attachments(event.attachments)
        self.message_text = event.message
        self.time = event.datetime

    def _get_sender_name(self, event: Event) -> str:
        name = self.db_holder.get_name(event.peer_id)
        if name == self.db_holder.NOT_FOUND:
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

        if "attach1_kind" in attachments and attachments["attach1_kind"] == "audiomsg":
            list_of_attachments.append(attachments["attach1_type"] + attachments["attach1"])
            self.is_it_voice_message = True
            return list_of_attachments

        for i in range(1, 11):
            attach_n_type = f"attach{i}_type"
            attach_n = f"attach{i}"
            if (attach_n_type in attachments and
                    (attachments[attach_n_type] == "photo" or attachments[attach_n_type] == "doc")):
                list_of_attachments.append(attachments[attach_n_type] + attachments[attach_n])
            else:
                return list_of_attachments

    def _get_sticker(self, attachments: dict) -> int:
        if "attach1_type" in attachments and attachments["attach1_type"] == "sticker":
            return attachments["attach1"]
        return 0

    def get_type(self):
        if self.sticker_id != 0:
            return self.STICKER
        if len(self.attachments) > 0 and type(self.attachments[0]) == Voice:
            return self.VOICE_MESSAGE
        return self.TEXT_MESSAGE

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