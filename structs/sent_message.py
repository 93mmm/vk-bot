from dataclasses import dataclass
from datetime import datetime


@dataclass
class SentMessage:
    def __init__(self, text: str, id_conversation: int, name_conversation: str):
        self.text = text
        self.id_conversation = id_conversation
        self.name_conversation = name_conversation
        self.time = datetime.now()

    def __str__(self):
        output = list()
        output.append(f"Sent message: {self.text}")
        output.append(f"In conversation: {self.id_conversation} ({self.name_conversation})")
        output.append(f"At this time: {self.time}\n\n")

        return "\n".join(output)
