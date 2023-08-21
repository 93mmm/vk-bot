from dataclasses import dataclass


@dataclass
class File:
    def __init__(self, path: str, conversation_id: int):
        self.conversation_id = conversation_id
        self.link = ""
        # TODO: load file https://ru.stackoverflow.com/questions/1265579/Отправка-документа-через-vk-api

    def load(self):
        self.link = ""

    def __str__(self):
        return f""