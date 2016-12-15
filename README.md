# Deprecated
This library is now outdated, I don't plan on updating it anymore and there must be better libraries to manage Telegram bots in Python.
# telegram-bot-api
Yet another event-based Python 3.X/Telegram-Bot-Api library. It's built and thought to be modular and plugin-based. Hook your own Handler and it'll receive updates according to the message type.

## Prerequisites
- Python 3
- requests module.

## Todo
- Auto-reloading plugins/handlers
- Add more API functions
- Investigate why the API doesn't send replies from X to Y and not to the bot.
- Document a little bit
- Document a little bit more
- Try to apply DRY
- Investigate how Python libraries work and (eventually) suggest this one once it became developped enough

## How the Update Api work?
A `Telegram` object has to be created and given as argument your bot's token and Telegram's API endpoint. After then you have to add handlers to this object with `addHandler(object)`. If an object implements one or more of the functions supported by `Telegram` update notifier, it'll be called on each of these functions.

### File uploading
Telegram's Bot API allow sending and resend documents on the same endpoints ("sendFOOBAR"), so the library functions act the same way.

- Sending the already sent document's `file_id` will send a resend request, avoiding to upload again the document for everyone. This seems (not totally tested yet) to work on every document type (as stickers for instance).
- Sending the document, like passing an `open("file", "rb")` (`rb` to avoid errors when trying to decode Unicode in binary files) to the function will upload the file to the servers. Make sure that your file hasn't been already downloaded as the servers doesn't check if it already exists and you'll get a new `file_id` as reply.

## Quick Example

Note : In this example, the API library is stored in `app/` folder.

```python
#!/usr/bin/python3
import configparser

from app.telegram import Telegram, Message
from app.handlers.loggerHandler import LoggerHandler


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        tg = Telegram(config["Telegram"]["apiURL"],config["Telegram"]["token"])
        loggerHandler = LoggerHandler("chat.log")
        tg.addHandler(loggerHandler)
        tg.processUpdates()
    except:
        print("There had been a problem while reading configuration file, please make sure that a config.ini file exists in the same folder than this one and that it follow the right configuration structure.")
```
