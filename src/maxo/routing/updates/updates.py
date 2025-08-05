from maxo.routing.updates.bot_added import BotAdded
from maxo.routing.updates.bot_removed import BotRemoved
from maxo.routing.updates.bot_started import BotStarted
from maxo.routing.updates.chat_title_changed import ChatTitileChanged
from maxo.routing.updates.message_callback import MessageCallback
from maxo.routing.updates.message_chat_created import MessageChatCreated
from maxo.routing.updates.message_created import MessageCreated
from maxo.routing.updates.message_edited import MessageEdited
from maxo.routing.updates.message_removed import MessageRemoved
from maxo.routing.updates.user_added import UserAdded
from maxo.routing.updates.user_removed import UserRemoved

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
)
