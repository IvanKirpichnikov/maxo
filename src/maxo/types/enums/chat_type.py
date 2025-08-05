from enum import StrEnum


class ChatType(StrEnum):
    """
    Тип чата.

    Attributes:
        CHAT: Групповой чат.
        DIALOG: Личный чат.

    """

    CHAT = "chat"
    DIALOG = "dialog"
