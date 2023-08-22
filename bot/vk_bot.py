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
        self.config = structs.LaunchConfig()
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
        self.log = logger.LogsWriter()
        self.messages = json_cfg.JsonMessagesHolder()

    def main(self):
        if self.config.configure_ids:
            self.get_all_conversations()
        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        peer_id = event.peer_id
                        self.log_received_message(event)
                        if self.config.collect_stickers:
                            self.check_sticker(peer_id, event.attachments)

                        if self.config.collect_messages:
                            pass  # TODO: collect messages

                        if self.config.collect_voices:
                            pass  # TODO: collect voices

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
            except ReadTimeout:
                pass
            except Exception as ex:
                self.log.log_exception(structs.ExceptionData(ex))
                sleep(2)

    def log_received_message(self, event: Event):
        received_message = structs.ReceivedMessage(event.text,
                                                   event.user_id,
                                                   self.get_sender_name(event.user_id, event.from_user),
                                                   event.peer_id,
                                                   self.get_conversation_name(event.peer_id))
        self.log.log_received(received_message)

    def get_sender_name(self, user_id: int, from_user: bool):
        # TODO: check if message from community
        if from_user:
            return "Bot's account"
        user = self.api.users.get(user_ids=str(user_id))[0]
        user = f"{user['first_name']} {user['last_name']}"
        return user

    def get_conversation_name(self, peer_id: int):
        # TODO: check if message from community
        response = self.api.messages.getConversationsById(peer_ids=peer_id,
                                                          extended=1,
                                                          fields="chat_settings")
        peer = response["items"][0]["peer"]
        if peer["type"] == "chat":
            return response["items"][0]["chat_settings"]["title"]
        elif peer["type"] == "user":
            profiles = response["profiles"]
            return f"{profiles[0]['first_name']} {profiles[0]['last_name']}"

    def check_sticker(self, peer_id: int, atts: dict):
        if "attach1_type" in atts and atts["attach1_type"] == "sticker" and peer_id in self.config.collect_stickers_from:
            #self.json_messages.append_sticker(int(atts["attach1"]))
            pass
        # TODO: rewrite json messages holder

    def get_all_conversations(self):
        def log_percents(percent, message):
            print("\r" + " " * 50, f"\r{percent}%, {message}", end="")
        
        configured_list_of_ids_path = "files/ids/configured_list_of_ids.txt"
        offset = 0
        receive = 200
        total_conversations = self.api.messages.getConversations(offset=offset,
                                                                 count=0,
                                                                 extended=1,
                                                                 fields="first_name, last_name")["count"]
        collected_data = list()
        collected_data.append("USER ID\t\tNAME OF CHAT\n")

        log_percents(50, "requesting data")
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

            log_percents(60, "creating a list with conversations")
            sleep(1)
        
        with open(configured_list_of_ids_path, "w") as file:
            log_percents(90, "creating a file with conversations")
            file.write("\n".join(collected_data))

        log_percents(100, f"rCreated file: {configured_list_of_ids_path}")
        exit()
