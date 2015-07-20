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
        self.loopingUpdateHandler = False
        self.lastID = 0
        self.handlers = []

    def send_request(self, action, params):
        url = "{}{}/{}".format(self.api_url, self.access_token, action)
        r = requests.get(url, params=params)
        try:
            return r.json()
        except ValueError:
            print("There has been a parsing error on this message : {}"
                  .format(r.text))
            return {"ok": False,
                    "why": "Parsing Error",
                    "message": r.text}

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

    def get_me(self):
        return self.send_request("getMe")

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

    def process_updates(self):
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
