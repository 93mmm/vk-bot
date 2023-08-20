# Нow do I fill in ```config.json```?

> [!IMPORTANT]
> Paste your token

- Get [acces token](https://vkhost.github.io) of your account
- Paste it instead of ```your-token``` in ```token``` field in ```config.json```
<br><br>

> [!IMPORTANT]
> if you want to receive and save messages from conferences

- Get the ID of the dialogs you want to get data from. Run script with flags:
```bash
python3 main.py -receive-only-ids
```
and check console messages (you will receive a text file)

Fill in ```config.json``` according to where you want to receive and save certain messages from:
```json
    "collect-stickers-from": [
        200004,
        6950606
    ],
    "collect-voices-from": [
        200004,
        200003,
        6859494
    ],
    "collect-messages-from": [
        200004,
        200003,
        6950606,
        6859494
    ]
```
<br><br>
> [!IMPORTANT]
> if you want to send spam to conferences

Fill in the ```send-spam-to``` field in the form of ”key: value", where the key is the conversation ID, the value is the number of messages between the bot messages:
```json
    "send-spam-to": {
        20004: 20,
        20005: 32
    },
```

Example of file ```config.json```:
```json
{
    "token": "your-token",
    "send-spam-to": {
        "200004": "20",
        "200003": "34"
    },
    "collect-stickers-from": [
        200004,
        6950606
    ],
    "collect-voices-from": [
        200004,
        200003,
        6859494
    ],
    "collect-messages-from": [
        200004,
        200003,
        6950606,
        6859494
    ]
}
```