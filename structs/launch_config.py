from dataclasses import dataclass
import json
import argparse

CONFIG = "files/json/config.json"


@dataclass
class LaunchConfig:
    def __init__(self):
        with open(CONFIG) as file:
            info = json.load(file)
        self.token = info["token"]
        self.conference_ids_to_monitor = info["conference-ids-to-monitor"]

        self.args = self.get_props()
        self.send_spam = self.args.send_spam
        self.collect_stickers = self.args.collect_stickers
        self.collect_voices = self.args.collect_voices
        self.collect_messages = self.args.collect_messages
        self.remove_subscriptions = self.args.remove_subscriptions
        self.remove_friends = self.args.remove_friends

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
                                       "(in the config.json file) from which messages need to be recorded")

        vk_bot_tools.add_argument("-collect-voices",
                                  action="store_true",
                                  help="receive and record incoming voices (you can configure a list of group IDs "
                                       "(in the config.json file) from which messages need to be recorded")

        vk_bot_tools.add_argument("-collect-messages",
                                  action="store_true",
                                  help="receive and record incoming messages (you can configure a list of group IDs "
                                       "(in the config.json file) from which messages need to be recorded)")

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
        config.append(f"-send-spam: {self.send_spam}")
        config.append(f"-collect-stickers: {self.collect_stickers}")
        config.append(f"-collect-voices: {self.collect_voices}")
        config.append(f"-collect-messages: {self.collect_messages}")
        config.append(f"-remove-all-subscriptions: {self.remove_subscriptions}")
        config.append(f"-remove-all-friends: {self.remove_friends}")
        return "\n\t".join(config)

    def check_config(self):
        pass
        # TODO: check flag's compatibility
