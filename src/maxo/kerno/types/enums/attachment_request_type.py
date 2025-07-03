from enum import Enum


class AttachmentRequestType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"
    STICKER = "sticker"
    CONTECT = "contact"
    INLINE_KEYBOARD = "inline_keyboard"
    LOCATION = "location"
    SHARE = "share"
