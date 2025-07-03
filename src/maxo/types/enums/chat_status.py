from enum import Enum


class ChatStatusType(str, Enum):
    ACTIVE = "active"
    REMOVED = "removed"
    LEFT = "left"
    CLOSED = "closed"
    SUSPENDED = "suspended"
