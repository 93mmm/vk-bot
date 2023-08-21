# Нow do I fill in ```config.json```?

> [!IMPORTANT]
> Paste your token

- Get [access token](https://vkhost.github.io) of your account
- Paste it instead of ```your-token``` in ```token``` field in ```config.json```
<br>

> [!IMPORTANT]
> if you want to receive and save messages from conferences

- Get the ID of the dialogs you want to get data from. Ignores chats with groups. Run script with flag:
```bash
python3 main.py -receive-only-ids
```
and check console messages (you will receive a text file)

Fill in ```config.json``` according to where you want to receive and save certain messages from:
```json
    "collect-stickers-from": [
        2000000024,
        1
    ],
    "collect-voices-from": [
        2000000024,
        2000000110,
        1
    ],
    "collect-messages-from": [
        2000000024,
        2000000110,
        1,
        2
    ]
```
<br>
> [!IMPORTANT]
> If you want to send spam to conferences

Fill in the ```send-spam-to``` field in the form of ”key: value", where the key is the conversation ID, the value is the number of messages between the bot messages:
```json
    "send-spam-to": {
        "2000000024": "20",
        "2000000110": "32"
    },
```

Example of file ```config.json```:
```json
{
    "token": "your-token",
    "send-spam-to": {
        "2000000024": "20",
        "2000000110": "32"
    },
    "collect-stickers-from": [
        2000000024,
        1
    ],
    "collect-voices-from": [
        2000000024,
        2000000110,
        1
    ],
    "collect-messages-from": [
        2000000024,
        2000000110,
        1,
        2
    ]
}
```
