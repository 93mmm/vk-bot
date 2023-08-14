# VK pseudo spam bot

Sends pseudo-spam messages into selected chat(s)

Collects recieved messages to a special file



## Requirements
vk-api:

```bash
pip3 install vk-api
```

## How to run?

> [!IMPORTANT]
> Configure environment

1. get [acces token](https://vkhost.github.io) of your account

2. paste it into the tokens section in the [```config.json```](https://github.com/93mmm/vk-pseudo-spam-bot/blob/main/json/config.json) file

3. configure your messages in the file [```messages.json```](https://github.com/93mmm/vk-pseudo-spam-bot/blob/main/json/messages.json)

4. add files into assets folder

5. select launch-mode mode in the [```config.json```](https://github.com/93mmm/vk-pseudo-spam-bot/blob/main/json/config.json)


| Mode      | Meaning |
------- | -------
| send-spam | starts spamming |
| collect-stickers-ids | send stickers on behalf of your account, and it will automatically add them to a special file |
| colect-voices | loads voices into [```assets/voices```](https://github.com/93mmm/vk-pseudo-spam-bot/tree/main/assets/voices) |
| collect-messages | fills [```assets```](https://github.com/93mmm/vk-pseudo-spam-bot/tree/main/assets) folder, [```messages.json```](https://github.com/93mmm/vk-pseudo-spam-bot/blob/main/json/messages.json) file with received messages |


6. run ```pip3 install vk-api```
7. listen to errors displayed in console

