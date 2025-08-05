from enum import StrEnum


class KeyboardButtonType(StrEnum):
    CALLBACK = "callback"
    CHAT = "chat"
    LINK = "link"
    REQUEST_GEO_LOCATION = "request_geo_location"
    REQUEST_CONTACT = "request_contact"
    MESSAGE = "message"
    OPEN_APP = "open_app"
