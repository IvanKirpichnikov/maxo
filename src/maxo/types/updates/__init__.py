from maxo.types.updates.bot_added import BotAdded
from maxo.types.updates.bot_removed import BotRemoved
from maxo.types.updates.bot_started import BotStarted
from maxo.types.updates.chat_title_changed import ChatTitileChanged
from maxo.types.updates.dialog_cleared import DialogCleared
from maxo.types.updates.message_callback import MessageCallback
from maxo.types.updates.message_chat_created import MessageChatCreated
from maxo.types.updates.message_created import MessageCreated
from maxo.types.updates.message_edited import MessageEdited
from maxo.types.updates.message_removed import MessageRemoved
from maxo.types.updates.user_added import UserAdded
from maxo.types.updates.user_removed import UserRemoved

Updates = (
    BotAdded
    | UserAdded
    | MessageRemoved
    | MessageEdited
    | MessageCallback
    | MessageChatCreated
    | MessageCreated
    | BotStarted
    | BotRemoved
    | ChatTitileChanged
    | UserRemoved
    | DialogCleared
)
