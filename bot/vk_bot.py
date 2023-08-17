import logger
import json_cfg
import structs

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
        self.config = json_cfg.RunConfig()

        try:
            print("connecting...")
            self.vk = VkApi(token=self.config.token)
            self.api = self.vk.get_api()
            self.longpoll = VkLongPoll(self.vk)
            print("success")
        except ApiError:
            # TODO: warnings.warn
            red = "\033[1;31;40m"
            red_end = "\033[0m"
            print(f"{red}Check your token{red_end}")
            exit()
        except ConnectionError:
            red = "\033[1;31;40m"
            red_end = "\033[0m"
            print(f"{red}Check your internet connection{red_end}")
            exit()

    def main(self):
        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW:
                        try:
                            print(event.attachments["attachments"])
                        except Exception as ex:
                            print(repr(ex))
                        self.log_received_message(event)
            except KeyboardInterrupt:
                print("\nKeyboard interrupt received, exiting.")
                exit()
            except Exception as ex:
                self.log.log_exception(structs.ExceptionData(ex))
                print("Exception occurred")
                sleep(2)

    def log_received_message(self, event: Event):
        received_message = structs.ReceivedMessage(event.text,
                                                   event.user_id,
                                                   self.get_sender_name(event),
                                                   event.peer_id,
                                                   self.get_conversation_name(event))
        self.log.log_received(received_message)

    def get_sender_name(self, event: Event):
        user = self.api.users.get(user_ids=str(event.user_id))[0]
        user = f"{user['first_name']} {user['last_name']}"
        return user

    def get_conversation_name(self, event: Event):
        conv_name = self.api.messages.getConversationsById(peer_ids=event.peer_id,
                                                           extended=1,
                                                           fields="chat_settings")
        if event.from_user:
            return f"{conv_name['profiles'][0]['first_name']} {conv_name['profiles'][0]['last_name']}"
        return conv_name["items"][0]["chat_settings"]["title"]
