from .telegram import Telegram, Message


class TelegramUpdateFetcher():
    """A update fetcher using Telegram's Bot API"""
    def __init__(self, tg):
        self.tg = tg
        self.loopingUpdateHandler = False
        self.lastID = 0
        
    def process_updates(self):
        self.loopingUpdateHandler = True
        while self.loopingUpdateHandler:
            notifications = self.tg.get_updates(self.lastID)
            if notifications["ok"] is True:
                for notification in notifications['result']:
                    self.lastID = max(self.lastID, notification["update_id"])+1
                    message = Message(notification["message"])
                    self.tg.call_handlers(message)
            else:
                print("Oops, something went bad : {}".format(notifications))
        
