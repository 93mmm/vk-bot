from structs import *

import tests
from helpers import write_json, log_percents, exit_from_script, colored_text
from const import *

from vk_api import VkApi
from vk_api.vk_api import VkApiMethod
from vk_api.exceptions import ApiError
from vk_api.longpoll import VkLongPoll, VkEventType

from time import sleep, time
from requests import ConnectionError
from threading import Thread


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
        tests.test()

        try:
            self.vk = VkApi(token=self.config.token)
            self.api = self.vk.get_api()
            self.longpoll = VkLongPoll(self.vk)
            print(colored_text("Connected to VK server", color="G"))
        except ApiError:
            exit_from_script("Check your token")
        except ConnectionError:
            exit_from_script("Check your internet connection")
        self.messages = JsonMessagesHolder()

    def main(self):
        if self.config.configure_ids:
            self.get_all_conversations()

        if self.config.change_statuses:
            changing_status_thread = Thread(target=self.change_status)
            changing_status_thread.start()

        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                        peer_id = event.peer_id
                        message = ReceivedMessage(self.vk, event)
                        if self.config.log_messages:
                            log_received(message)
                        print(message)

                        if self.config.to_collect_sticker(peer_id, message.get_type()):
                            self.messages.add_new_message(message)

                        if self.config.to_collect_message(peer_id, message.get_type()):
                            self.messages.add_new_message(message, save_attachments=True)

                        if self.config.to_collect_voices(peer_id, message.get_type()):
                            self.messages.add_new_message(message, save_attachments=True)
                        
                        # TODO: collect only docs

                        if self.config.send_spam:
                            if peer_id in self.config.current_received:
                                print(self.config.current_received)
                                if self.config.current_received[peer_id] == self.config.spam_delay[peer_id]:
                                    self.config.current_received[peer_id] = 0
                                    self.messages.generate_random_message(self.vk, peer_id).send(self.api)
                                else:
                                    self.config.current_received[peer_id] += 1
            except KeyboardInterrupt:
                exit_from_script()
            except ConnectionError:
                sleep(2)
            except Exception as ex:
                log_exception(Ex(ex))
                sleep(2)
    
    def change_status(self):
        offset = 0
        while True:
            self.api.status.set(text=self.config.statuses[offset])
            sleep(self.config.status_change_period)
            offset += 1
            offset %= len(self.config.statuses)
            print("changed")

    def get_all_conversations(self):
        log_percents(10, "Requesting data..")
        collected_data_dict = dict()
        collected_data_list = list()

        offset = 0
        receive = 200
        total_conversations = self.api.messages.getConversations(offset=offset,
                                                                 count=0,
                                                                 extended=1,
                                                                 fields="first_name, last_name")["count"]
        
        collected_data_list.append("USER ID\t\tNAME OF CHAT\n")
        log_percents(50, "Requesting data...")
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

            log_percents(60, "Creating a list with conversations...")
            sleep(1)
        
        with open(CONVERSATIONS_TXT, "w") as file:
            log_percents(90, "Creating a file with conversations")
            file.write("\n".join(collected_data_list))
        
        write_json(CONVERSATIONS_JSON, collected_data_dict)

        log_percents(100, f"Created file: {CONVERSATIONS_TXT}")
        exit_from_script()
