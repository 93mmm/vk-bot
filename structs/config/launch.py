import argparse

from const import CONFIG_JSON, RECEIVED_MESSAGES_FILE, STICKER, VOICE_MESSAGE, TEXT_MESSAGE
from helpers import read_json, colored_text, exit_from_script


class LaunchConfig:
    def __init__(self):
        json_data = read_json(CONFIG_JSON)

        self.token: str = None
        self.spam_delay: dict = None
        self.current_received: dict = None

        self.statuses: list[str] = None
        self.status_change_period: int = None

        self.collect_stickers_from: set = None
        self.collect_voices_from: set = None
        self.collect_messages_from: set = None

        self.token = json_data["token"]
        self.spam_delay, self.current_received = self._configure(json_data["send-spam-to"])
        # if send-spam-to is empty: warn
        # TODO: check if delay = 0 in spam_delay

        self.statuses: list[str] = json_data["status"]["statuses"]
        self.status_change_period: int = json_data["status"]["period"]

        self.collect_stickers_from = set(json_data["collect-stickers-from"])
        self.collect_voices_from = set(json_data["collect-voices-from"])
        self.collect_messages_from = set(json_data["collect-messages-from"])

        args = self._get_props()
        self.send_spam = args.send_spam
        self.change_statuses = args.change_statuses
        self.log_messages = args.log_messages
        self.configure_ids = args.configure_ids

        self._collect_stickers = args.collect_stickers
        self._collect_voices = args.collect_voices
        self._collect_messages = args.collect_messages
        self._load_only_docs = args.load_only_docs
        self._remove_subscriptions = args.remove_subscriptions
        self._remove_friends = args.remove_friends
        self._remove_videos = args.remove_videos

        self._check_config()
    
    def to_collect_sticker(self, peer_id: int, type: int) -> bool:
        return (self._collect_stickers and
                type is STICKER and
                (peer_id in self.collect_stickers_from or len(self.collect_stickers_from) == 0)
                )

    def to_collect_message(self, peer_id: int, type: int) -> bool:
        return (self._collect_messages and
                type is TEXT_MESSAGE and
                (peer_id in self.collect_messages_from or len(self.collect_messages_from) == 0)
                )
    
    def to_collect_voices(self, peer_id: int, type: int) -> bool:
        return (self._collect_voices and
                type is VOICE_MESSAGE and
                (peer_id in self.collect_voices_from or len(self.collect_voices_from) == 0)
                )

    def _check_config(self):
        # TODO: add "u will collect messages from: {id} {name}"
        config = list()
        e = False
        config.append(colored_text("Selected config:", color="G"))
        if self.send_spam:
            config.append("-send-spam")
        if self._collect_stickers:
            config.append("-collect-stickers")
        if self._collect_voices:
            config.append("-collect-voices")
        if self._collect_messages:
            config.append("-collect-messages")
        if self._load_only_docs:
            config.append("-load-only-docs")
        if self.change_statuses:
            config.append("-change-statuses")
        if self.log_messages:
            config.append("-log-messages")
        if self.configure_ids:
            config.append("-configure-ids")
        if self._remove_subscriptions:
            config.append("-remove-subscriptions")
        if self._remove_friends:
            config.append("-remove-friends")
        if self._remove_videos:
            config.append("-remove-videos")
        if len(config) == 1:
            config.append(colored_text("You have not selected the bot launch options, "
                                       "the bot won't do anything.",
                                       color="R"))
            e = True
        print("\n\t".join(config))
        if e:
            exit_from_script()
    
        bot_tools = [self.send_spam, self._collect_stickers, self._collect_voices,
                     self._collect_messages, self._load_only_docs, self.change_statuses]
        page_tools = [self._remove_subscriptions, self._remove_friends, self._remove_videos]

        if any(bot_tools) and any(page_tools):
            exit_from_script("Selected incompatible options, please read docs and re-select options")

        elif self.configure_ids and len(bot_tools) + len(page_tools) >= 1:
            print(colored_text("You selected -configure-ids option, the code will be stopped after "
                  "configuring file and other options will give no effect", color="B"))

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

        vk_bot_tools.add_argument("-change-statuses",
                                  action="store_true",
                                  help="change the status of the page once in a certain period")

        vk_bot_tools.add_argument("-log-messages",
                                  action="store_true",
                                  help=f"log all received messages into a file ({RECEIVED_MESSAGES_FILE})")

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
