from enum import Enum
from datetime import datetime

# Considering only text rn, but in the future, we may need this
class MessageType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    STICKER = "sticker"
    GIF = "gif"
    FILE = "file"
    LOCATION = "location"

class Message:
    def __init__(self, sender: str, recipient: str, text, timestamp: datetime, message_type: MessageType, media_url=None, read=False, replied_to=None):
        self.sender = sender  # Username of the sender
        self.recipient = recipient # Username of the recipient
        self.text = text  # Text content of the message
        self.timestamp = timestamp  # Timestamp of when the message was sent
        self.message_type = message_type
        self.media_url = media_url  # URL of the media if the message is an image, video, etc.
        self.read = read  # Boolean indicating if the message has been read
        self.replied_to = replied_to  # Reference to the message this one is replying to
    
    def mark_as_read(self):
        self.read = True

    def __str__(self):
        return f"Message(sender={self.sender}, text={self.text}, timestamp={self.timestamp}, type={self.message_type}, read={self.read})"
