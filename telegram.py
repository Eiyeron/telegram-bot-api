import requests
import sys
from .models import Message


class Telegram:
    """This class wraps the (almost) whole Telegram API and offers a
    handler-based update system to plug to the interface whatever functionality
    you want."""
    # TODO ? : Convert this into a simple array
    # and get value by doing "on_"+"value"
    handlerTypeCallback = {
        "update": "on_update",
        "forward_from": "on_forward",
        "reply_to_message": "on_reply",
        "text": "on_text",
        "audio": "on_audio",
        "document": "on_document",
        "photo": "on_photo",
        "sticker": "on_sticker",
        "video": "on_video",
        "contact": "on_contact",
        "location": "on_location",
        "new_chat_participant": "on_new_chat_carticipant",
        "left_chat_participant": "on_left_chat_participant",
        "new_chat_title": "on_new_chat_title",
        "new_chat_photo": "on_new_chat_photo",
        "delete_chat_Photo": "on_delete_chat_photo",
        "group_chat_created": "on_group_chat_created",
    }

    def __init__(self, api_url, token):
        self.api_url = api_url
        self.access_token = token
        self.loopingUpdateHandler = False
        self.lastID = 0
        self.handlers = []

    def send_request(self, action, params={}, files=[]):
        """Wraps the url building and sends the requst to Telegram's servers.
        Returns the processed data in JSON or a JSON object containing the
        error message."""
        url = "{}{}/{}".format(self.api_url, self.access_token, action)
        r = requests.get(url, params=params, files=files)
        try:
            return r.json()
        except ValueError:
            print("There has been a parsing error on this message : {}"
                  .format(r.text))
            return {"ok": False,
                    "why": "Parsing Error",
                    "message": r.text}

    def send_file(self, chat_id, command, method, file_data,
                  reply_to_message_id="",
                  reply_markup=""):
        """Wraps the file sending process."""
        args = {"chat_id": chat_id,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup}
        files = {}
        # Checking if it's a resend id.
        if isinstance(file_data, str):
            args[method] = file_data
        else:
            files[method] = file_data
        return self.send_request(command, args, files)

    def get_updates(self, offset=0, limit=100, timeout=0):
        """Using /getUpdates to poll updates from Telegram."""
        return self.send_request("getUpdates", {"offset": offset,
                                                "limit": limit,
                                                "timeout": timeout})

    def send_message(self, chat_id, text,
                     reply_to_message=None,
                     reply_markup=None):
        """Sends a text-only message to a chat/user."""
        params = {"chat_id": chat_id, "text": text}
        if reply_to_message is not None:
            params["reply_to_message"] = reply_to_message

        if reply_markup is not None:
            params["reply_markup"] = reply_markup

        return self.send_request("sendMessage", params)

    def forward_message(self, chat_id, from_chat_id, message_id):
        """Forwards a message from a chat to another chat."""
        return self.send_request("forwardMessage",
                                 {"chat_id": chat_id,
                                  "from_chat_id": from_chat_id,
                                  "message_id": message_id})

    def get_me(self):
        """Returns the basic infos about the bot. Good function for testing
        if communicating to Telegram works."""
        return self.send_request("getMe")

    def send_photo(self, chat_id, photo,
                   reply_to_message_id="", reply_markup=""):
        """Sends a photo the "quick way", a client will receive a smaller,
        compressed version of the original file. Prefer send_document if
        you need the original version to be sent."""
        return self.send_file(chat_id, "sendPhoto", "photo", photo,
                              reply_to_message_id, reply_markup)

    def send_audio(self, chat_id, audio,
                   reply_to_message_id="", reply_markup=""):
        """Sends an audio file."""
        return self.send_file(chat_id, "sendAudio", "audio", audio,
                              reply_to_message_id, reply_markup)

    def send_document(self, chat_id, document,
                      reply_to_message_id="", reply_markup=""):
        """Sends a document, whatever its filetype is. Perfect for sending
        pictures without affecting their quality/size, GIFs, or all the files
        you want."""
        return self.send_file(chat_id, "sendDocument", "document", document,
                              reply_to_message_id, reply_markup)

    def send_sticker(self, chat_id, sticker,
                     reply_to_message_id="", reply_markup=""):
        """Sends a sticker to the given chat. You have to find a way
        to know the sticker id before as no infos are given on them
        unless you were sent one."""
        return self.send_file(chat_id, "sendSticker", "sticker", sticker,
                              reply_to_message_id, reply_markup)

    def send_video(self, chat_id, video,
                   reply_to_message_id="", reply_markup=""):
        """Sends a video. Looks like Telegram's servers compress
        and scale down them. Prefer send_document if you need the
        original version to be sent."""
        return self.send_file(chat_id, "sendVideo", "video", video,
                              reply_to_message_id, reply_markup)

    def send_location(self, chat_id, latitude, longitude,
                      reply_to_message_id="", reply_markup=""):
        """Sends a location. The client will see a map frame with
        given location"""
        return self.send_request("sendLocation",
                                 {"chat_id": chat_id,
                                  "latitude": latitude,
                                  "longitude": longitude,
                                  "reply_to_message_id": reply_to_message_id,
                                  "reply_to_message_id": reply_markup
                                  })

    def add_handler(self, handler):
        """Adds a update handler to the current instance."""
        if "callback" not in self.handlers:
            self.handlers.append(handler)

    def remove_handler(self, callback, **kwargs):
        """Checks if the handlers exists and removes it."""
        if callback in self.handlers:
            self.handlers.remove(callback)

    def call_handlers(self, message):
        """Internal function to notifiy handlers based on their
        implemented entry points."""
        for handler in self.handlers:
            for k, v in self.handlerTypeCallback.items():
                if (k == "update" or hasattr(message, k))\
                   and hasattr(handler, v):
                    try:
                        getattr(handler, v)(self, message)
                    except:
                        print("""Oops, there has been a problem
                              with this handler : {}""".format(handler))
                        print(sys.exc_info())

    def process_updates(self):
        """Pools updates and dispatches them to the handlers."""
        self.loopingUpdateHandler = True
        while self.loopingUpdateHandler:
            notifications = self.get_updates(self.lastID)
            if notifications["ok"] is True:
                for notification in notifications['result']:
                    self.lastID = max(self.lastID, notification["update_id"])+1
                    message = Message(notification["message"])
                    self.call_handlers(message)
            else:
                print("Oops, something went bad : {}".format(notifications))
