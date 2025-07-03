from enum import Enum


class MessageLinkType(str, Enum):
    REPLY = "reply"
    FORWARD = "forward"
