import argparse
from sys import exit

from const import CONFIG_JSON
from helpers import read_json



class LaunchConfig:
    def __init__(self):
        json_data = read_json(CONFIG_JSON)

        self.token: str = None
        self.delay: dict = None
        self.current_received: dict = None

        self.collect_stickers_from: set = None
        self.collect_voices_from: set = None
        self.collect_messages_from: set = None

        self.token = json_data["token"]
        self.delay, self.current_received = self._configure(json_data["send-spam-to"])

        self.collect_stickers_from = set(json_data["collect-stickers-from"])
        self.collect_voices_from = set(json_data["collect-voices-from"])
        self.collect_messages_from = set(json_data["collect-messages-from"])

        args = self._get_props()
        self.send_spam = args.send_spam
        self.collect_stickers = args.collect_stickers
        self.collect_voices = args.collect_voices
        self.collect_messages = args.collect_messages
        self.load_only_docs = args.load_only_docs
        self.configure_ids = args.configure_ids
        self.remove_subscriptions = args.remove_subscriptions
        self.remove_friends = args.remove_friends
        self.remove_videos = args.remove_videos

        # TODO: add flag for creating message logs

    def check_config(self):
        print(str(self))
        bot_tools = [self.send_spam, self.collect_stickers, self.collect_voices,
                     self.collect_messages, self.load_only_docs]
        page_tools = [self.remove_subscriptions, self.remove_friends, self.remove_videos]
        if any(bot_tools) and any(page_tools):
            print("Selected incompatible options, please read docs and re-select options")
            exit()
        elif self.configure_ids and len(bot_tools) + len(page_tools) >= 1:
            print("You selected -configure-ids option, the code will be stopped after "
                  "configuring file and other options will give no effect")

    def _configure(self, from_what: dict):
        delay, current_received = dict(), dict()
        for key, value in from_what.items():
            key = int(key)
            delay[key] = value
            current_received[key] = 0
        return delay, current_received

    def _get_props(self):
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
                                       f"(in the {CONFIG_JSON} file) from which messages need to be recorded")

        vk_bot_tools.add_argument("-collect-voices",
                                  action="store_true",
                                  help="receive and record incoming voices (you can configure a list of group IDs "
                                       f"(in the {CONFIG_JSON} file) from which messages need to be recorded")

        vk_bot_tools.add_argument("-collect-messages",
                                  action="store_true",
                                  help="receive and record incoming messages (you can configure a list of group IDs "
                                       f"(in the {CONFIG_JSON} file) from which messages need to be recorded)")

        vk_bot_tools.add_argument("-load-only-docs",
                                  action="store_true",
                                  help="receive and write to memory only documents")

        vk_page_tools.add_argument("-configure-ids",
                                   action="store_true",
                                   help="listen to the console output to get the IDs and names of conversations")

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
        if self.load_only_docs:
            config.append("-load-only-docs")
        if self.configure_ids:
            config.append("-configure-ids")
        if self.remove_subscriptions:
            config.append("-remove-subscriptions")
        if self.remove_friends:
            config.append("-remove-friends")
        if self.remove_videos:
            config.append("-remove-videos")
        if len(config) == 1:
            config.append("You have not selected the bot launch options, the bot will simply receive and log messages.")
        return "\n\t".join(config)

