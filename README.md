# VK pseudo spam bot

- [x] Sends spam to selected conferences through a certain interval in messages
- [ ] Collects stickers sent in selected conversations
- [ ] Collects voice messages sent in selected conversations
- [ ] Collects messages sent in selected conversations
- [x] Composes a special file that contains the ID and names of all chats of the account (ignores chats with communities)
- [ ] Deletes all subscriptions from the account
- [ ] Removes all friends from the account (leaves them in subscribers)
- [ ] Removes all added videos from the account

## Requirements
```bash
pip3 install -r requirements.txt
```

## How to run?

> [!IMPORTANT]
> Configure environment

1. Configure [```config.json```](https://github.com/93mmm/vk-pseudo-spam-bot/tree/master/files/json) file to start script

2. Type ```python3 main.py {flags}``` to run script

## Flags

```bash
python3 main.py -h
```



| Flag                    | Description                                                                                                                                                 |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `-send-spam`            | send messages to specified groups after receiving some number of messages from them                                                                         |
| `-collect-stickers`     | receive and record incoming stickers (you can configure a list of group IDs (in the `files/json/config.json` file) from which messages need to be recorded  |
| `-collect-voices`       | receive and record incoming voices (you can configure a list of group IDs (in the `files/json/config.json` file) from which messages need to be recorded    |
| `-collect-messages`     | receive and record incoming messages (you can configure a list of group IDs (in the `files/json/config.json` file) from which messages need to be recorded) |
| `-load-only-docs`       | load all received docs into memory (does not collect messages in a `files/json/messages.json`)                                                              |
| `-receive-only-ids`     | listen to the console output to get the IDs and names of conversations (you can improve application's logging speed by creating one)                        |
| `-remove-subscriptions` | remove all subscriptions from your account                                                                                                                  |
| `-remove-friends`       | remove all friends from your account                                                                                                                        |
| `-remove-videos`        | remove all added videos from your account                                                                                                                   |
