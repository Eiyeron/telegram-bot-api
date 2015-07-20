from datetime import datetime


class LoggerHandler:

    def __init__(self, filename):
        try:
            self.file = open(filename, 'a')
        except IOError:
            self.file = None
            print("Couldn't open {} for log writing".format(filename))

    def on_text(self, tg, message):
        if self.file is not None:
            date = datetime.fromtimestamp(message.date)\
                .strftime('%Y-%m-%d %H:%M:%S')
            self.file.write("[{}]{} : {}\n"
                            .format(date,
                                    message.from_user.first_name,
                                    message.text))
            self.file.flush()

    def on_sticker(self, tg, message):
        date = datetime.fromtimestamp(message.date)\
                .strftime('%Y-%m-%d %H:%M:%S')
        self.file.write("[{}]{} sent a sticker (id:{}).\n"
                        .format(date,
                                message.from_user.username,
                                message.sticker.file_id))
        self.file.flush()
