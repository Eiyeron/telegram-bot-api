class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data.get("last_name", "")
        self.username = data.get("username", "")


class GroupChat:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]


class Message:
    def __init__(self, data):
        self.message_id = data["message_id"]
        self.from_user = User(data["from"])
        self.date = data["date"]

        # Finding if we have a GroupChat or an User
        if "title" in data["chat"]:
            self.chat = GroupChat(data["chat"])
        elif "first_name" in data["chat"]:
            self.chat = User(data["chat"])

        # Forward data
        # Idea : as date is there if there is from,
        # move date into from's condition?
        if "forward_from" in data:
            self.forward_from = User(data["forward_from"])

        if "forward_date" in data:
            self.forward_date = data["forward_date"]

        # Message types
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

        # What happened in the server
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


# Todo? Keyboard superclass for inheritance
class ReplyKeybaordMarkup:
    def __init__(self, data):
        self.keyboard = []
        for row in data["keyboard"]:
            self.keyboard.append(list(row))
            self.reisze_keyboard = data.get("resize_keyboard", False)
            self.one_time_keyboard = data.get("one_time_keyboard", False)
            self.selective = data.get("selective", False)


class ReplyKeyboardHide:
    def __init__(self, data):
        self.force_reply = data["force_reply"]
        self.selective = data.get("selective", False)
