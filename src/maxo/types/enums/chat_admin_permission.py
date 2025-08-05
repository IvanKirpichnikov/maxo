from enum import Enum


class ChatAdminPermission(Enum):
    """
    Перечень прав пользователя.

    Attributes:
        READ_ALL_MESSAGES: Читать все сообщения.
        ADD_REMOVE_MEMBERS: Добавлять/удалять участников.
        ADD_ADMINS: Добавлять администраторов.
        CHANGE_CHAT_INFO: Изменять информацию о чате.
        PIN_MESSAGE: Закреплять сообщения.
        WRITE: Писать сообщения.

    """

    READ_ALL_MESSAGES = "read_all_messages"
    ADD_REMOVE_MEMBERS = "add_remove_members"
    ADD_ADMINS = "add_admins"
    CHANGE_CHAT_INFO = "change_chat_info"
    PIN_MESSAGE = "pin_message"
    WRITE = "write"
