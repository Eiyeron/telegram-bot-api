class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        if "last_name" in data:
            self.last_name = data["last_name"]
        else:
            self.last_name = ""
        if "username" in data:
            self.username = data["username"]
        else:
            slef.username = ""

class GroupChat:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]

class Message:
    def __init__(self, data):
        self.message_id = data["message_id"]
        self.from_user = User(data["from"])
        self.date = data["date"]
        if "title" in data["chat"]:
            self.chat = GroupChat(data["chat"])
        elif "first_name" in data["chat"]:
            self.chat = User(data["chat"])
        if "forward_from" in data:
            self.forward_from = User(data["forward_from"])
        if "forward_date" in data:
            self.forward_date = data["forward_date"]
        if "reply_to_message" in data:
            self.reply_to_message = Message(data["reply_to_message"])
        if "text" in data:
            self.text = data["text"]
        if "audio" in data:
            self.audio = Audio(data["audio"])
        if "document" in data:
            self.document = Document(data["document"])
        if "photo" in data:
            self.photo = []
            for photo in data["photo"]:
                self.photo.append(PhotoSize(photo))
        if "sticker" in data:
            self.sticker = Sticker(data["sticker"])
        if "video" in data:
            self.video = Video(data["video"])
        if "contact" in data:
            self.contact = Contact(data["contact"])
        if "location" in data:
            self.location = Location(data["location"])
        if "new_chat_participant" in data:
            self.new_chat_participant = User(data["new_chat_participant"])
        if "left_chat_participant" in data:
            self.left_chat_participant = User(data["left_chat_participant"])
        if "new_chat_title" in data:
            self.new_chat_title = data["new_chat_title"]
        if "new_chat_photo" in data:
            self.new_chat_photo = []
            for photo in data["new_chat_photo"]:
                self.new_chat_photo.append(PhotoSize(photo))
        if "delete_chat_photo" in data:
            self.delete_chat_photo = data["delete_chat_photo"]
        if "group_chat_created" in data:
            self.group_chat_created = data["group_chat_created"]



# Todo? : Inheritance and create a File superclass for all file-related classes?

class PhotoSize:
    def __init__(self, data):
        if not data: return
        self.file_id = data["file_id"]
        self.width = data["width"]
        self.height = data["height"]
        if "file_size" in data:
            self.file_size = data["file_size"]
        else:
            self.file_size = -1

class Audio:
    def __init__(self, data):
        self.file_id = data["file_id"]
        self.duration = data["duration"]
        self.mime_type = data["mime_type"]
        if "file_size" in data:
            self.file_size = data["file_size"]
        else:
            self.file_size = -1

class Document:
    def __init__(self, data):
       self.file_id = data["file_id"]
       self.thumb = PhotoSize(data["thumb"])
       if "file_name" in data:
           self.file_name = data["file_name"]
       else:
           self.file_name = ""
       if "mime_type" in data:
           self.mime_type = data["mime_type"]
       else:
           self.mime_type = ""
       if "file_size" in data:
           self.file_size = data["file_size"]
       else:
           self.file_size = -1

class Sticker:
    def __init__(self, data):
        self.file_id = data["file_id"]
        self.width = data["width"]
        self.height = data["height"]
        self.thumb = PhotoSize(data["thumb"])
        if "file_size" in data:
            self.file_size = data["file_size"]
        else:
            self.file_size = -1

class Video:
    def __init__(self, data):
        self.file_id = data["file_id"]
        self.width = data["width"]
        self.height = data["height"]
        self.duration = data["duration"]
        self.thumb = PhotoSize(data["thumb"])
        if "mime_type" in data:
           self.mime_type = data["mime_type"]
        else:
           self.mime_type = ""
        if "file_size" in data:
           self.file_size = data["file_size"]
        else:
           self.file_size = -1
        if "caption" in data:
           self.caption = data["caption"]
        else:
           self.caption = ""

class Contact:
    def __init__(self, data):
        self.phone_number = data["phone_number"]
        self.first_name = data["first_name"]
        if "last_name" in data:
           self.last_name = data["last_name"]
        else:
           self.last_name = ""
        if "user_id" in data:
           self.user_id = data["user_id"]
        else:
           self.user_id = ""

class Location:
    def __init__(self, data):
        self.longitude = data["longitude"]
        self.latitude = data["latitude"]

class UserProfilePhotos:
    def __init__(self, data):
        self.total_count = data["total_count"]
        self.photos = []
        for slice in data["photos"]:
            line = []
            for photo in slice:
                line.append(PhotoSize(photo))
            self.photos.append(line)

# Todo? Keyboard superclass for inheritance

class ReplyKeybaordMarkup:
    def __init__(self, data):
        self.keyboard = []
        for slice in data["keyboard"]:
            line = []
            for key in slice:
                line.append(key)
            self.keyboard.append(line)
        if "resize_keyboard" in data:
            self.resize_keyboard = data["resize_keybaord"]
        else:
            self.resize_keybaord = False
        if "one_time_keybaord" in data:
            self.one_time_keybaord = data["one_time_keybaord"]
        else:
            self.one_time_keybaord = False
        if "selective" in data:
            self.selective = data["selective"]
        else:
            self.selective = False

class ReplyKeyboardHide:
    def __init__(self, data):
        self.force_reply = data["force_reply"]
        if "selective" in data:
            self.selective = data["selective"]
        else:
            self.selective = False

