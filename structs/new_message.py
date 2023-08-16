from dataclasses import dataclass
import vk_api


@dataclass
class TextMessage:
    def __init__(self, conversation_id: int, text: str, attachments: list):
        self.conversation_id = conversation_id
        self.text = text
        self.attachments = attachments

    def send(self, api: vk_api.VkApi):
        pass
        # TODO: send constructed message

    def append_attachment(self, att):
        self.attachments.append(att)

    def join_attachments(self):
        pass
        # TODO: join all attachments into string


@dataclass
class Sticker:
    def __init__(self, conversation_id: int, sticker_id: int):
        self.conversation_id = conversation_id
        self.sticker_id = sticker_id

    def send(self, vk):
        pass
        # TODO: send sticker


@dataclass
class Voice:
    def __init__(self, conversation_id: int, path: str):
        pass

    def send(self):
        pass