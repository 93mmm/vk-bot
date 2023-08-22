from logger.filenames import *


class LogsWriter:
    def __init__(self):
        pass

    def log_exception(self, strct):
        with open(EXCEPTIONS, "a") as file:
            file.write(str(strct))
        print(strct.ex.__class__)

    def log_received(self, strct):
        with open(RECEIVED_MESSAGES, "a") as file:
            file.write(str(strct))

    def log_sent(self, strct):
        with open(SENT_MESSAGES, "a") as file:
            file.write(str(strct))

    def renew_files(self):
        with open(EXCEPTIONS, "w"):
            pass

        with open(RECEIVED_MESSAGES, "w"):
            pass

        with open(SENT_MESSAGES, "w"):
            pass
