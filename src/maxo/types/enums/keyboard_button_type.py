from enum import Enum


class KeyboardButtonType(str, Enum):
    CALLBACK = "callback"
    LINK = "link"
    REQUEST_GEO_LOCATION = "request_geo_location"
    REQUEST_CONTACT = "request_contact"
    CHAT = "chat"
