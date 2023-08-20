from dataclasses import dataclass
import json
import argparse
from sys import exit

CONFIG = "files/json/config.json"


@dataclass
class LaunchConfig:
    def __init__(self):
        with open(CONFIG) as file:
            info = json.load(file)
        self.token = info["token"]
        self.send_spam_to = info["send-spam-to"]

        self.args = self.get_props()
        self.send_spam = self.args.send_spam
        self.collect_stickers = self.args.collect_stickers
        self.collect_voices = self.args.collect_voices
        self.collect_messages = self.args.collect_messages
        self.receive_only_ids = self.args.receive_only_ids
        self.remove_subscriptions = self.args.remove_subscriptions
        self.remove_friends = self.args.remove_friends
        self.remove_videos = self.args.remove_videos

    def get_props(self):
        parser = argparse.ArgumentParser(
            prog='vk-bot',
            description='does some useless shit with vk api',
            epilog='https://github.com/93mmm/vk-pseudo-spam-bot')
        vk_bot_tools = parser.add_argument_group("vk_bot_tools")
        vk_page_tools = parser.add_argument_group("vk_page_tools")

        vk_bot_tools.add_argument("-send-spam",
                                  action="store_true",
                                  help="send messages to specified groups after receiving some number of messages from "
                                       "them")

        vk_bot_tools.add_argument("-collect-stickers",
                                  action="store_true",
                                  help="receive and record incoming stickers (you can configure a list of group IDs "
                                       f"(in the {CONFIG} file) from which messages need to be recorded")

        vk_bot_tools.add_argument("-collect-voices",
                                  action="store_true",
                                  help="receive and record incoming voices (you can configure a list of group IDs "
                                       f"(in the {CONFIG} file) from which messages need to be recorded")

        vk_bot_tools.add_argument("-collect-messages",
                                  action="store_true",
                                  help="receive and record incoming messages (you can configure a list of group IDs "
                                       f"(in the {CONFIG} file) from which messages need to be recorded)")

        vk_page_tools.add_argument("-receive-only-ids",
                                   action="store_true",
                                   help="listen to the console output to get the IDs and names of conversations")

        # TODO: configure file  ID | NAME_OF_CONVERSATION
        vk_page_tools.add_argument("-remove-subscriptions",
                                   action="store_true",
                                   help="remove all subscriptions from your account")

        vk_page_tools.add_argument("-remove-friends",
                                   action="store_true",
                                   help="remove all friends from your account")

        vk_page_tools.add_argument("-remove-videos",
                                   action="store_true",
                                   help="remove all added videos from your account")

        return parser.parse_args()

    def __str__(self):
        config = list()
        config.append("Selected config:")
        if self.send_spam:
            config.append("-send-spam")
        if self.collect_stickers:
            config.append("-collect-stickers")
        if self.collect_voices:
            config.append("-collect-voices")
        if self.collect_messages:
            config.append("-collect-messages")
        if self.receive_only_ids:
            config.append("-receive-spam")
        if self.remove_subscriptions:
            config.append("-remove-subscriptions")
        if self.remove_friends:
            config.append("-remove-friends")
        if self.remove_videos:
            config.append("-remove-videos")
        return "\n\t".join(config)

    def check_config(self):
        print(str(self))
        bot_tools = [self.send_spam, self.collect_stickers, self.collect_voices, self.collect_messages]
        page_tools = [self.receive_only_ids, self.remove_subscriptions, self.remove_friends, self.remove_videos]
        if any(bot_tools) and any(page_tools):
            print("Selected incompatible options, please read docs and re-select options")
            exit()
