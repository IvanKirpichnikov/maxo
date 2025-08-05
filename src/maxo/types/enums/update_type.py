from enum import StrEnum


class UpdateType(StrEnum):
    MESSAGE_CREATED = "message_created"
    MESSAGE_CALLBACK = "message_callback"
    MESSAGE_EDITED = "message_edited"
    MESSAGE_REMOVED = "message_removed"
    BOT_ADDED = "bot_added"
    BOT_REMOVED = "bot_removed"
    USER_ADDED = "user_added"
    USER_REMOVED = "user_removed"
    BOT_STARTED = "bot_started"
    CHAT_TITLE_CHANGED = "chat_title_changed"
    MESSAGE_CHAT_CREATED = "message_chat_created"
    DIALOG_CLEARED = "dialog_cleared"
