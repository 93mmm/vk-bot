from custom_logs.filenames import *

class LogsWriter:
    def __init__(self):
        self.error_f = open(ERRORS, "a")
        self.received_msg_f = open(RECEIVED_MESSAGES, "a")
        self.sent_msg_f = open(SENT_MESSAGES, "a")
    
    def __del__(self):
        self.error_f.close()
        self.received_msg_f.close()
        self.sent_msg_f.close()

    def log_exception(self, strct):
        self.error_f.write(str(strct))

    def log_received(self, strct):
        self.received_msg_f.write(str(strct))

    def log_sent(self, strct):
        self.sent_msg_f.write(str(strct))

    def renew_files(self):
        with open(ERRORS, "w") as file:
            file.write("")

        with open(RECEIVED_MESSAGES, "w") as file:
            file.write("")

        with open(SENT_MESSAGES, "w") as file:
            file.write("")

        print("files cleared")