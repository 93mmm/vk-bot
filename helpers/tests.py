from os import path

from const import *
from helpers import read_json, write_json, free_file, exit_from_script, warn, colored_text


def check_and_warn_about_errors_in_json_files():
    data = read_json(CONFIG_JSON)
    give_instructions = False

    if not data["token"].startswith("vk1.a."):
        warn(f"check your token field in {CONFIG_JSON}")
        give_instructions = True

    for field in ["send-spam-to", "collect-stickers-from", "collect-voices-from", "collect-messages-from"]:
        if data[field] == list() or data[field] == dict():
            warn(f"field \"{field}\" in {CONFIG_JSON} is empty")
            give_instructions = True
    
    if data["status"]["period"] < 5:
        warn(f"field \"period\" in field \"status\" in {CONFIG_JSON} is less than 5 sec. Config edited to valid version.")
        data["status"]["period"] = 5
        write_json(data)
        give_instructions = True

    if len(data["status"]["statuses"]) <= 1:
        warn(f"\"statuses\" in field \"status\" in {CONFIG_JSON} has only one status to change. Add more statuses.")
        give_instructions = True

    if give_instructions:
        print(colored_text("Check instructions on GitHub at link: https://github.com/93mmm/vk-bot/blob/master/files/json/README.md", color="b"))
        print(colored_text("Anyway, you can disable this warning by adding flag -dsq", color="g"))


def renew_logs_files():
    for fl in [EXCEPTIONS_FILE, RECEIVED_MESSAGES_FILE, SENT_MESSAGES_FILE]:
        free_file(fl)


def check_files():
    messages = read_json(MESSAGES_JSON)
    to_exit = False
    for msg in messages:
        if "photos" in msg:
            for photo in msg["photos"]:
                photo = PHOTOS_PATH + photo
                if not path.exists(photo):
                    warn(f"File {photo} is not exists")
                    to_exit = True
        if "files" in msg:
            for doc in msg["files"]:
                doc = DOCS_PATH + doc
                if not path.exists(doc):
                    warn(f"File {doc} is not exists")
                    to_exit = True
        if "voice-message" in msg:
            vm = VOICE_PATH + msg["voice-message"]
            if not path.exists(vm):
                warn(f"File {vm} is not exists")
                to_exit = True

    if to_exit:
        exit_from_script()
