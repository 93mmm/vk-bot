from include.const import *
import json

class LogsWriter:
    def __init__(self):

        self.err_f = open(ERRORS_FILE, "w")
        with open(ERRORS_FILE, "r") as file:
            self.err_f_data = file.readlines()

        self.rec_msg_f = open(RECIEVED_MESSAGES_FILE, "w")
        with open(RECIEVED_MESSAGES_FILE, "r") as file:
            self.rec_msg_f_data = file.readlines()

        self.sent_msg_f = open(SENT_MESSAGES_FILE, "w")
        with open(SENT_MESSAGES_FILE, "r") as file:
            self.sent_msg_f_data = file.readlines()
    
    def __del__(self):
        self.err_f.close()
        self.rec_msg_f.close()
        self.sent_msg_f.close()
        print('class destroyed')

    def log_exception(*line):
        # TODO: wrap line and write into file
        " ".join(line)
        print(line)

    def log_sent(*line):
        # TODO: wrap line and write into file
        " ".join(line)
        print(line)
    
    def log_received(*line):
        # TODO: wrap line and write into file
        " ".join(line)
        print(line)
    
    def renew_files(self):
        self.err_f.write(ERRORS_FILE_FIRST_LINE)
        self.rec_msg_f.write(RECIEVED_MESSAGES_FILE_FIRST_LINE)
        self.sent_msg_f.write(SENT_MESSAGES_FILE_FIRST_LINE)
        print("files cleared")


class MessagesJsonHolder:
    def __init__(self):
        with open(MESSAGES_FILE) as file:
            self.messages = json.load(file)

    def get_random_message(self):
        pass # TODO: choice sticker or message or voice
        # TODO: return message as class
