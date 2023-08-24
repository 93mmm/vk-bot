from random import randint
from structs.attachment_types import *
from datetime import datetime


class TextMessage:
    def __init__(self, peer_id: int, attachments: list[Voice | Doc | Photo], text="", sticker_id=0):
        self.peer_id: int = None
        self.attachments: list[Voice | Doc | Photo] = None
        self.text: str = None
        self.sticker_id: int = None

        self.peer_id = peer_id
        self.attachments = attachments
        self.text = text
        self.sticker_id = sticker_id
    
    def send(self, api):
        for index, element in self.attachments:
            self.attachments = self.attachments[index].send()

        api.messages.send(peer_id=self.peer_id, 
                          random_id=randint(0, 100000),
                          message=self.text, 
                          attachment=",".join(self.attachments),
                          sticker_id=self.sticker_id)

    def __str__(self):
        output = list()
        if self.text != "":
            output.append(f"Text: {self.text}")
        if self.sticker_id != 0:
            output.append(f"Sticker: {self.sticker_id}")

        output.append(f"To: {self.peer_id}")
        atts = "Attachments"
        if len(self.attachments) != 0:
            attachments = " | ".join(list(map(str, self.attachments)))
            output.append(f"{atts}: {attachments}")
        output.append(f"At the time: {datetime.now()}\n\n")

        return "\n".join(output)