import requests
import sys
from .models import Message


class Telegram:
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
        self.handlers = []

    def send_request(self, action, params, files=[]):
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
        args = {"chat_id": chat_id,
                "reply_to_message_id": reply_to_message_id,
                "reply_markup": reply_markup}
        files = {}
        if isinstance(file_data, str):
            args[method] = file_data
        else:
            files[method] = file_data
        return self.send_request(command, args, files)

    def get_updates(self, offset=0, limit=100, timeout=0):
        return self.send_request("getUpdates", {"offset": offset,
                                                "limit": limit,
                                                "timeout": timeout})

    def send_message(self, chat_id, text,
                     reply_to_message=None,
                     reply_markup=None):
        params = {"chat_id": chat_id, "text": text}
        if reply_to_message is not None:
            params["reply_to_message"] = reply_to_message

        if reply_markup is not None:
            params["reply_markup"] = reply_markup

        return self.send_request("sendMessage", params)

    def forward_message(self, chat_id, from_chat_id, message_id):
        return self.send_request("forwardMessage",
                                 {"chat_id": chat_id,
                                  "from_chat_id": from_chat_id,
                                  "message_id": message_id})

    def send_photo(self, chat_id, photo,
                   reply_to_message_id="", reply_markup=""):
        return self.send_file(chat_id, "sendPhoto", "photo", photo,
                              reply_to_message_id, reply_markup)

    def send_audio(self, chat_id, audio,
                   reply_to_message_id="", reply_markup=""):
        return self.send_file(chat_id, "sendAudio", "audio", audio,
                              reply_to_message_id, reply_markup)

    def send_document(self, chat_id, document,
                      reply_to_message_id="", reply_markup=""):
        return self.send_file(chat_id, "sendDocument", "document", document,
                              reply_to_message_id, reply_markup)

    def send_sticker(self, chat_id, sticker,
                     reply_to_message_id="", reply_markup=""):
        return self.send_file(chat_id, "sendSticker", "sticker", sticker,
                              reply_to_message_id, reply_markup)

    def send_video(self, chat_id, video,
                   reply_to_message_id="", reply_markup=""):
        return self.send_file(chat_id, "sendVideo", "video", video,
                              reply_to_message_id, reply_markup)

    def send_location(self, chat_id, latitude, longitude,
                      reply_to_message_id="", reply_markup=""):
        return self.send_request(chat_id, {"latitude": latitude,
                                           "longitude": longitude})

    def add_handler(self, handler):
        if "callback" not in self.handlers:
            self.handlers.append(handler)

    def remove_handler(self, callback, **kwargs):
        if callback in self.handlers:
            self.handlers.remove(callback)

    def call_handlers(self, message):
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

