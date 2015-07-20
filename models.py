# Using __dict__ and *args for compulsory args and **kwargs for optional ones.


class User(object):
    def __init__(self, *args):
        try:
            self.__dict__ = args[0]
        except:
            pass


class GroupChat(object):
    def __init__(self, *args):
        try:
            self.__dict__ = args[0]
        except:
            pass


# Todo? : Inheritance and create a File superclass
# for all file-related classes?
class PhotoSize:
    def __init__(self, data):
        if not data:
            return
        self.file_id = data["file_id"]
        self.width = data["width"]
        self.height = data["height"]
        self.file_size = data.get("file_size", -1)


class Audio:
    def __init__(self, data):
        self.file_id = data["file_id"]
        self.duration = data["duration"]
        self.mime_type = data["mime_type"]
        self.file_size = data.get("file_size", -1)


class Document:
    def __init__(self, data):
        self.file_id = data["file_id"]
        self.thumb = PhotoSize(data["thumb"])
        self.file_name = data.get("file_name", "")
        self.mime_type = data.get("mime_type", "")
        self.file_size = data.get("file_size", -1)


class Sticker:
    def __init__(self, data):
        self.file_id = data["file_id"]
        self.width = data["width"]
        self.height = data["height"]
        self.thumb = PhotoSize(data["thumb"])
        self.file_size = data.get("file_size", -1)


class Video:
    def __init__(self, data):
        self.file_id = data["file_id"]
        self.width = data["width"]
        self.height = data["height"]
        self.duration = data["duration"]
        self.thumb = PhotoSize(data["thumb"])
        self.mime_type = data.get("mime_type", "")
        self.file_size = data.get("file_size", -1)
        self.caption = data.get("caption", "")


class Contact:
    def __init__(self, data):
        self.phone_number = data["phone_number"]
        self.first_name = data["first_name"]
        self.last_name = data.get("last_name", "")
        self.user_id = data.get("user_id", "")


class Location:
    def __init__(self, data):
        self.longitude = data["longitude"]
        self.latitude = data["latitude"]


class UserProfilePhotos:
    def __init__(self, data):
        self.total_count = data["total_count"]
        self.photos = []
        for row in data["photos"]:
            self.photos.append(list(row))


class ReplyKeyBoard(object):
    def __init__(self, **kwargs):
        self.selective = kwargs.get('selective', False)


class ReplyKeyboardMarkup(ReplyKeyBoard):

    def __init__(self, keyboard, **kwargs):
        ReplyKeyBoard.__init__(self, **kwargs)
        self.keyboard = keyboard
        self.reisze_keyboard = kwargs.get("resize_keyboard", False)
        self.one_time_keyboard = kwargs.get("one_time_keyboard", False)


class ReplyKeyboardHide(ReplyKeyBoard):

    def __init__(self, **kwargs):
        ReplyKeyBoard.__init__(self, **kwargs)
        self.hide_keyboard = True


class ForceReply(ReplyKeyBoard):

    def __init__(self, **kwargs):
        ReplyKeyBoard.__init__(self, **kwargs)
        self.force_reply = True


replace_dict = {'forward_from': User,
                'audio': Audio,
                'document': Document,
                'sticker': Sticker,
                'video': Video,
                'contact': Contact,
                'location': Location,
                'new_chat_participant': User,
                'left_chat_participant': User
                }


class Message(object):
    def __init__(self, *args):
        message_dict = {}

        for attr, attr_value in args[0].items():

            if attr == 'from':
                message_dict['from_user'] = User(attr_value)
            elif attr == 'chat':
                # Finding if we have a GroupChat or an User
                if 'first_name' in attr_value:
                    message_dict[attr] = User(attr_value)
                elif 'title' in attr_value:
                    message_dict[attr] = GroupChat(attr_value)
            elif attr in replace_dict:
                message_dict[attr] = replace_dict[attr](attr_value)
            elif attr == "reply_to_message":
                message_dict[attr] = Message(attr_value)
            elif attr in ("photo", "new_chat_photo"):
                photos = []
                for photo in attr_value:
                    photos.append(PhotoSize(photo))
                message_dict[attr] = photos
            else:
                message_dict[attr] = attr_value

        self.__dict__ = message_dict
