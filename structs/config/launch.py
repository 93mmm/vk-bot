import argparse

from const import CONFIG_JSON, RECEIVED_MESSAGES_FILE, STICKER, VOICE_MESSAGE, TEXT_MESSAGE
from helpers import read_json, colored_text, exit_from_script


class LaunchConfig:
    def __init__(self):
        json_data = read_json(CONFIG_JSON)

        self._token: str = None
        self._spam_delay: dict = None
        self._current_received: dict = None

        self._statuses: list[str] = None
        self._status_change_period: int = None

        self._collect_stickers_from: set = None
        self._collect_voices_from: set = None
        self._collect_messages_from: set = None

        self._token = json_data["token"]
        self._spam_delay, self._current_received = self._configure(json_data["send-spam-to"])

        self._statuses: list[str] = json_data["status"]["statuses"]
        self._status_change_period: int = json_data["status"]["period"]

        self._collect_stickers_from = set(json_data["collect-stickers-from"])
        self._collect_voices_from = set(json_data["collect-voices-from"])
        self._collect_messages_from = set(json_data["collect-messages-from"])

        args = self._get_props()
        self._send_spam = args.send_spam
        self._change_statuses = args.change_statuses
        self._log_messages = args.log_messages
        self._configure_ids = args.configure_ids

        self._collect_stickers = args.collect_stickers
        self._collect_voices = args.collect_voices
        self._collect_messages = args.collect_messages
        self._load_only_docs = args.load_only_docs
        self._remove_subscriptions = args.remove_subscriptions
        self._remove_friends = args.remove_friends
        self._remove_videos = args.remove_videos
        self._disable_squiggles = args.disable_squiggles

        self._check_config()
    
    def to_collect_sticker(self, peer_id: int, type: int) -> bool:
        return (self._collect_stickers and
                type is STICKER and
                (peer_id in self._collect_stickers_from or len(self._collect_stickers_from) == 0)
                )

    def to_collect_message(self, peer_id: int, type: int) -> bool:
        return (self._collect_messages and
                type is TEXT_MESSAGE and
                (peer_id in self._collect_messages_from or len(self._collect_messages_from) == 0)
                )
    
    def to_collect_voices(self, peer_id: int, type: int) -> bool:
        return (self._collect_voices and
                type is VOICE_MESSAGE and
                (peer_id in self._collect_voices_from or len(self._collect_voices_from) == 0)
                )
    
    def to_spam_into(self, peer_id: int) -> bool:
        if self._send_spam and peer_id in self._current_received and self._current_received[peer_id] >= self._spam_delay[peer_id]:
            self._current_received[peer_id] = 0
            return True
        if peer_id in self._current_received:
            self._current_received[peer_id] += 1
        return False
    
    def to_change_statuses(self):
        return self._change_statuses
    
    def to_log_messages(self):
        return self._log_messages
    
    def to_configure_ids(self):
        return self._configure_ids
    
    def to_check_files(self):
        return self._disable_squiggles
    
    def to_load_only_docs(self):
        return self._load_only_docs
    
    def get_statuses_info(self) -> tuple:
        return self._status_change_period, *self._statuses
    
    def get_token(self):
        return self._token

    def _check_config(self):
        config = list()
        e = False
        config.append(colored_text("Selected config:", color="G"))
        if self._send_spam:
            config.append("-send-spam")
        if self._collect_stickers:
            config.append("-collect-stickers")
        if self._collect_voices:
            config.append("-collect-voices")
        if self._collect_messages:
            config.append("-collect-messages")
        if self._load_only_docs:
            config.append("-load-only-docs")
        if self._change_statuses:
            config.append("-change-statuses")
        if self._log_messages:
            config.append("-log-messages")
        if self._configure_ids:
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
    
        bot_tools = [self._send_spam, self._collect_stickers, self._collect_voices,
                     self._collect_messages, self._load_only_docs, self._change_statuses]
        page_tools = [self._remove_subscriptions, self._remove_friends, self._remove_videos]

        if any(bot_tools) and any(page_tools):
            exit_from_script("Selected incompatible options, please read docs and re-select options")

        elif self._configure_ids and len(bot_tools) + len(page_tools) >= 1:
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
            epilog='https://github.com/93mmm/vk-bot')
        vk_bot_tools = parser.add_argument_group("vk_bot_tools")
        vk_page_tools = parser.add_argument_group("vk_page_tools")
        debug_tools = parser.add_argument_group("debug_tools")

        vk_bot_tools.add_argument("-send-spam",
                                  "-ss",
                                  action="store_true",
                                  help="send messages to specified groups after receiving some number of messages from "
                                       "them")

        vk_bot_tools.add_argument("-collect-stickers",
                                  "-cs",
                                  action="store_true",
                                  help="receive and record incoming stickers (you can configure a list of group IDs "
                                       f"(in the {CONFIG_JSON} file) from which messages need to be recorded")

        vk_bot_tools.add_argument("-collect-voices",
                                  "-cv",
                                  action="store_true",
                                  help="receive and record incoming voices (you can configure a list of group IDs "
                                       f"(in the {CONFIG_JSON} file) from which messages need to be recorded")

        vk_bot_tools.add_argument("-collect-messages",
                                  "-cm",
                                  action="store_true",
                                  help="receive and record incoming messages (you can configure a list of group IDs "
                                       f"(in the {CONFIG_JSON} file) from which messages need to be recorded)")

        vk_bot_tools.add_argument("-load-only-docs",
                                  "-lod",
                                  action="store_true",
                                  help="receive and write to memory only documents")

        vk_page_tools.add_argument("-configure-ids",
                                   "-ci",
                                   action="store_true",
                                   help="listen to the console output to get the IDs and names of conversations")

        vk_page_tools.add_argument("-remove-subscriptions",
                                   "-rs",
                                   action="store_true",
                                   help="remove all subscriptions from your account")

        vk_page_tools.add_argument("-remove-friends",
                                   "-rf",
                                   action="store_true",
                                   help="remove all friends from your account")

        vk_page_tools.add_argument("-remove-videos",
                                   "-rv",
                                   action="store_true",
                                   help="remove all added videos from your account")

        vk_page_tools.add_argument("-change-statuses",
                                  "-chst",
                                  action="store_true",
                                  help="change the status of the page once in a certain period")

        debug_tools.add_argument("-disable-squiggles",
                                 "-dsq",
                                 action="store_true",
                                 help="disable error squiggles")
        
        debug_tools.add_argument("-log-messages",
                                 "-lm",
                                 action="store_true",
                                 help=f"log all received messages into a file ({RECEIVED_MESSAGES_FILE})")

        return parser.parse_args()
