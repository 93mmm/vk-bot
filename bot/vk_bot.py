import logger
import json_cfg
import structs
import tests

from vk_api import VkApi
from vk_api.exceptions import ApiError
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from time import sleep
from sys import exit
from requests import ConnectionError


class Bot:
    def __init__(self):
        self.log = logger.LogsWriter()
        self.json_messages = json_cfg.JsonMessagesHolder()
        self.config = structs.LaunchConfig()
        self.config.check_config()

        tests.test()

        try:
            print("connecting...")
            self.vk = VkApi(token=self.config.token)
            self.api = self.vk.get_api()
            self.longpoll = VkLongPoll(self.vk)
            print("success")
        except ApiError:
            print("Check your token")
            exit()
        except ConnectionError:
            print("Check your internet connection")
            exit()

        if self.config.receive_only_ids:
            self.get_all_conversations()

    def main(self):
        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        self.log_received_message(event)
                        if self.config.collect_stickers:
                            self.check_sticker(event.attachments)
                        if self.config.collect_messages:
                            pass  # TODO: collect messages
                        if self.config.collect_voices:
                            pass  # TODO: collect voices
                        if self.config.send_spam:
                            pass  # TODO: send spam
            except KeyboardInterrupt:
                print("\nKeyboard interrupt received, exiting.")
                exit()
            except ConnectionError as ex:
                self.log.log_exception(structs.ExceptionData(ex))
                sleep(2)
            except Exception as ex:
                self.log.log_exception(structs.ExceptionData(ex))
                print("Exception occurred")
                sleep(2)

    def log_received_message(self, event: Event):
        received_message = structs.ReceivedMessage(event.text,
                                                   event.user_id,
                                                   self.get_sender_name(event.user_id),
                                                   event.peer_id,
                                                   self.get_conversation_name(event.peer_id))
        self.log.log_received(received_message)

    def get_sender_name(self, user_id: int):
        user = self.api.users.get(user_ids=str(user_id))[0]
        user = f"{user['first_name']} {user['last_name']}"
        return user

    def get_conversation_name(self, peer_id: int):
        response = self.api.messages.getConversationsById(peer_ids=peer_id,
                                                          extended=1,
                                                          fields="chat_settings")
        peer = response["items"][0]["peer"]

        if peer["type"] == "chat":
            return response["items"][0]["chat_settings"]["title"]
        elif peer["type"] == "user":
            profiles = response["profiles"]
            idx = 0
            if profiles[1]["id"] == peer_id:
                idx = 1
            f"{profiles[idx]['first_name']} {profiles[idx]['last_name']}"

    def check_sticker(self, atts):
        if "attach1_type" in atts and atts["attach1_type"] == "sticker":
            self.json_messages.append_sticker(int(atts["attach1"]))

    def get_all_conversations(self):
        configured_list_of_ids_path = "files/ids/configured_list_of_ids.txt"
        print("receiving conversations...")
        offset = 0
        receive = 200
        print("\r" + " " * 50, "\r10%, requesting total number of conversations", end="")
        total_conversations = self.api.messages.getConversations(offset=offset,
                                                                 count=0,
                                                                 extended=1,
                                                                 fields="first_name, last_name")["count"]
        collected_data = list()
        collected_data.append("USER ID\t\tNAME OF CHAT\n")
        print("\r" + " " * 50, "\r30%, requesting data", end="")
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
                    collected_data.append(f"{peer_id}:\t{users[peer_id]}")
                elif peer["type"] == "chat":
                    collected_data.append(f"{peer_id}:\t{el['conversation']['chat_settings']['title']}")
            print("\r" + " " * 50, "\r50%, creating a list with conversations", end="")

            sleep(1)

        with open(configured_list_of_ids_path, "w") as file:
            print("\r" + " " * 50, "\r70%, creating a file with conversations", end="")
            file.write("\n".join(collected_data))
        print("\r" + " " * 50, f"\rCreated file: {configured_list_of_ids_path}")
        exit()
