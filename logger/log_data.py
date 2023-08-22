from logger.filenames import *
from structs import ExceptionData, ReceivedMessage, SentMessage
# TODO: make functions static


class LogsWriter:
    def __init__(self):
        pass

    def log_exception(self, strct: ExceptionData):
        with open(EXCEPTIONS, "a") as file:
            file.write(str(strct))
        print(strct.ex.__class__)

    def log_received(self, strct: ReceivedMessage):
        with open(RECEIVED_MESSAGES, "a") as file:
            file.write(str(strct))

    def log_sent(self, strct: SentMessage):
        with open(SENT_MESSAGES, "a") as file:
            file.write(str(strct))

    def renew_files(self):
        with open(EXCEPTIONS, "w"):
            pass

        with open(RECEIVED_MESSAGES, "w"):
            pass

        with open(SENT_MESSAGES, "w"):
            pass
