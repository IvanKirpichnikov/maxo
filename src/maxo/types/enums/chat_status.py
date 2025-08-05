from enum import StrEnum


class ChatStatusType(StrEnum):
    """
    Статус чата.

    Attributes:
        ACTIVE: Бот является активным участником чата.
        REMOVED: Бот был удалён из чата.
        LEFT: Бот покинул чат.
        CLOSED: Чат был закрыт.

    """

    ACTIVE = "active"
    REMOVED = "removed"
    LEFT = "left"
    CLOSED = "closed"
