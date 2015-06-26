import requests
from .models import Message

class Telegram:
    handlerTypeCallback = {
        "update":"onUpdate",
        "forward_from":"onForward",
        "reply_to_message":"onReply",
        "text":"onText",
        "audio":"onAudio",
        "document":"onDocument",
        "photo":"onPhoto",
        "sticker":"onSticker",
        "video":"onVideo",
        "contact":"onContact",
        "location":"onLocation",
        "new_chat_participant":"onNewChatParticipant",
        "left_chat_participant":"onLeftChatParticipant",
        "new_chat_title":"onNewChatTitle",
        "new_chat_photo":"onNewChatPhoto",
        "delete_chat_Photo":"onDeleteChatPhoto",
        "group_chat_created":"onGroupChatCreated",
    }
    def __init__(self, api_url, token):
        """docstring for __init__"""
        self.api_url = api_url
        self.access_token = token
        self.loopingUpdateHandler = False
        self.lastID = 0
        self.handlers = []

    def sendRequest(self, action, params):
        url = "{}{}/{}".format(self.api_url,self.access_token,action)
        r = requests.get(url, params=params)
        return r.json()

    def getUpdates(self, offset=0, limit=100, timeout=0):
        return self.sendRequest("getUpdates", {"offset":offset, "limit":limit, "timeout":timeout})

    def sendMessage(self, chat_id, text, reply_to_message=None, reply_markup=None):
        params = {"chat_id":chat_id, "text":text}
        if reply_to_message is not None:
            params["reply_to_message"] = reply_to_message
        if reply_markup is not None:
            params["reply_markup"] = reply_markup
        return self.sendRequest("sendMessage", params)

    def forwardMessage(self, chat_id, from_chat_id, message_id):
        return self.sendRequest("forwardMessage", {"chat_id":chat_id, "from_chat_id":from_chat_id, "message_id": message_id})

    def addHandler(self, handler):
        if not "callback" in self.handlers:
            self.handlers.append(handler)
    
    def removeHandler(self, callback, **kwargs):
        if callback in self.handlers:
            self.handlers.remove(callback)
    
    def processUpdates(self):
        loopingUpdateHandler = True
        while loopingUpdateHandler:
            notifications = self.getUpdates(self.lastID)
            if notifications["ok"] is True:
                for notification in notifications['result']:
                    self.lastID = max(self.lastID, notification["update_id"])+1
                    message = Message(notification["message"])
                    for handler in self.handlers:
                        for k,v in self.handlerTypeCallback.items():
                            if (k=="update" or hasattr(message, k)) and hasattr(handler, v):
                                try:
                                    getattr(handler, v)(self, message)
                                except:
                                    print("Oops, there has been a problem with this handler : {}".format(handler))
                                    print(sys.exc_info()[0])

            else:
                print("Oops, something went bad : {}".format(notification))

