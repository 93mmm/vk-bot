from structs import *
from helpers import *
from const import *

from vk_api import VkApi
from vk_api.vk_api import VkApiMethod
from vk_api.exceptions import ApiError
from vk_api.longpoll import VkLongPoll, VkEventType

from requests import ConnectionError
from threading import Thread


class Bot:
    def __init__(self):
        self.config: LaunchConfig = None
        self.vk: VkApi = None
        self.api: VkApiMethod = None
        self.longpoll: VkLongPoll = None
        self.messages: JsonMessagesHolder = None

        renew_logs_files()
        check_files()

        self.config = LaunchConfig()
        if not self.config.to_check_files():
            check_and_warn_about_errors_in_json_files()

        try:
            self.vk = VkApi(token=self.config.get_token())
            self.api = self.vk.get_api()
            self.longpoll = VkLongPoll(self.vk)
            print(colored_text("Connected to VK server", color="G"))
        except ApiError:
            exit_from_script("Check your token")
        except ConnectionError:
            exit_from_script("Check your internet connection")
        self.messages = JsonMessagesHolder()

    def main(self):
        if self.config.to_configure_ids():
            self.get_all_conversations()

        if self.config.to_change_statuses():
            changing_status_thread = Thread(target=self.change_status, daemon=True)
            changing_status_thread.start()

        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                        peer_id = event.peer_id
                        message = ReceivedMessage(self.vk, event)
                        if self.config.to_log_messages():
                            log_received(str(message))

                        if self.config.to_collect_sticker(peer_id, message.get_type()):
                            self.messages.add_new_message(message)

                        if self.config.to_collect_message(peer_id, message.get_type()):
                            self.messages.add_new_message(message, save_attachments=True)

                        if self.config.to_collect_voices(peer_id, message.get_type()):
                            self.messages.add_new_message(message, save_attachments=True)
                        
                        if self.config.to_load_only_docs():
                            message.download_attachments()
                        
                        if self.config.to_spam_into(peer_id):
                            th = Thread(target=self.messages.generate_random_message(self.vk, peer_id).send, args=[self.api])
                            th.start()

            except KeyboardInterrupt:
                exit_from_script()
            except ConnectionError:
                sleep(2)
            except Exception as ex:
                log_exception(repr(Ex(ex)))
                sleep(2)
    
    def change_status(self):
        delay, *statuses = self.config.get_statuses_info()
        offset = 0
        if delay < 5:
            delay = 5
        while True:
            self.api.status.set(text=statuses[offset])
            sleep(delay)
            offset = (offset + 1) % len(statuses)

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
        log_percents(20, "Requesting data...")
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

            log_percents(20 + offset // 20, "Creating a list with conversations...")
            sleep(1)
        
        log_percents(90, "Creating a file with conversations")

        write_lines(CONVERSATIONS_TXT, *collected_data_list, delimiter="\n")
        write_json(CONVERSATION_CACHES, collected_data_dict)

        log_percents(100, f"Created file: {CONVERSATIONS_TXT}")
        exit_from_script()
