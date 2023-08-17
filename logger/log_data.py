from logger.filenames import *


class LogsWriter:
    def __init__(self):
        pass

    def log_exception(self, strct):
        with open(EXCEPTIONS, "a") as file:
            file.write(str(strct))
        # TODO: warning: exc occurred

    def log_received(self, strct):
        with open(RECEIVED_MESSAGES, "a") as file:
            file.write(str(strct))

    def log_sent(self, strct):
        with open(SENT_MESSAGES, "a") as file:
            file.write(str(strct))

    def renew_files(self):
        with open(EXCEPTIONS, "w") as file:
            file.write("")

        with open(RECEIVED_MESSAGES, "w") as file:
            file.write("")

        with open(SENT_MESSAGES, "w") as file:
            file.write("")

        print("files cleared")
