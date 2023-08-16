from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExceptionData:
    def __init__(self, ex, **variables):
        self.ex = ex
        self.variables = variables

    def __str__(self):
        message = f"Thrown exception: {repr(self.ex)}\nVariables:\n"
        for key, value in self.variables.items():
            message += f"{key} = {value}\n"
        return message + "\n"


@dataclass
class ReceivedMessage:
    def __init__(self, text: str, id_from: int, name_from: str, id_conversation: int, name_conversation: str):
        self.text = text
        self.id_from = id_from
        self.name_from = name_from
        self.id_conversation = id_conversation
        self.name_conversation = name_conversation
        self.time = datetime.now()

    def __str__(self):
        output = list()
        output.append(f"Received message: {self.text}")
        output.append(f"From user: {self.id_from} ({self.name_from})")
        output.append(f"In conversation: {self.id_conversation} ({self.name_conversation})")
        output.append(f"At this time: {self.time}\n\n")

        return "\n".join(output)


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
