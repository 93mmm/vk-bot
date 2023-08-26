from structs import *

import tests
from helpers import write_json
from const import *

from vk_api import VkApi
from vk_api.vk_api import VkApiMethod
from vk_api.exceptions import ApiError
from vk_api.longpoll import VkLongPoll, VkEventType

from time import sleep
from sys import exit
from requests import ConnectionError


def log_exception(strct: Ex):
    with open(EXCEPTIONS_FILE, "a") as file:
        file.write(str(strct))
    print(repr(strct.ex))

def log_received(strct: ReceivedMessage):
    with open(RECEIVED_MESSAGES_FILE, "a") as file:
        file.write(str(strct))

def log_sent(strct: SentMessage):
    with open(SENT_MESSAGES_FILE, "a") as file:
        file.write(str(strct))


class Bot:
    def __init__(self):
        self.config: LaunchConfig = None
        self.vk: VkApi = None
        self.api: VkApiMethod = None
        self.longpoll: VkLongPoll = None
        self.messages: JsonMessagesHolder = None

        self.config = LaunchConfig()
        self.config.check_config()
        tests.test()

        try:
            self.vk = VkApi(token=self.config.token)
            self.api = self.vk.get_api()
            self.longpoll = VkLongPoll(self.vk)
            print("Connected to VK server")
        except ApiError:
            print("Check your token")
            exit()
        except ConnectionError:
            print("Check your internet connection")
            exit()
        self.messages = JsonMessagesHolder()

    def main(self):
        if self.config.configure_ids:
            self.get_all_conversations()
        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                        peer_id = event.peer_id
                        message = ReceivedMessage(self.vk, event)
                        log_received(message)

                        if self.config.collect_stickers and message.get_type() == ReceivedMessage.STICKER:
                            self.messages.add_new_message(message)

                        if self.config.collect_messages:
                            self.messages.add_new_message(message, save_attachments=True)

                        if self.config.collect_voices and message.get_type() == ReceivedMessage.VOICE_MESSAGE:
                            self.messages.add_new_message(message, save_attachments=True)
                        
                        # TODO: collect only docs

                        if self.config.send_spam:
                            if peer_id in self.config.current_received:
                                if self.config.current_received[peer_id] == self.config.delay[peer_id]:
                                    self.config.current_received[peer_id] = 0
                                    self.messages.generate_random_message(self.vk, peer_id).send(self.api)
                                else:
                                    self.config.current_received[peer_id] += 1
            except KeyboardInterrupt:
                print("\nKeyboard interrupt received, exiting.")
                exit()
            except ConnectionError as ex:
                sleep(2)
            except Exception as ex:
                log_exception(Ex(ex))
                sleep(2)

    def get_all_conversations(self):
        def log_percents(percentage: int, message: str):
            print("\r" + " " * 50, f"\r{percentage}%, {message}", end="")
        
        collected_data_dict = dict()
        collected_data_list = list()

        offset = 0
        receive = 200
        total_conversations = self.api.messages.getConversations(offset=offset,
                                                                 count=0,
                                                                 extended=1,
                                                                 fields="first_name, last_name")["count"]
        
        collected_data_list.append("USER ID\t\tNAME OF CHAT\n")
        log_percents(50, "requesting data")
        # TODO: optimize
        while total_conversations > offset:
            conversations = self.api.messages.getConversations(offset=offset,
                                                               count=receive,
                                                               extended=1,
                                                               fields="first_name, last_name")
            offset += receive
            users = dict()
            for el in conversations["profiles"]:
                users[str(el["id"])] = f"{el['first_name']} {el['last_name']}"

            for el in conversations["items"]:
                peer = el["conversation"]["peer"]
                peer_id = str(peer["id"])

                if peer["type"] == "user":
                    usr = users[peer_id]
                    collected_data_dict[peer_id] = usr
                    collected_data_list.append(f"{peer_id}:\t{usr}")
                elif peer["type"] == "chat":
                    usr = el['conversation']['chat_settings']['title']
                    collected_data_dict[peer_id] = usr
                    collected_data_list.append(f"{peer_id}:\t{usr}")

            log_percents(60, "creating a list with conversations")
            sleep(1)
        
        with open(CONVERSATIONS_TXT, "w") as file:
            log_percents(90, "creating a file with conversations")
            file.write("\n".join(collected_data_list))
        
        write_json(CONVERSATIONS_JSON, collected_data_dict)

        log_percents(100, f"Created file: {CONVERSATIONS_TXT}")
        exit()
