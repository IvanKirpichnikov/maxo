from typing import Any, Final

from maxo.kerno.routing.ctx import Ctx
from maxo.kerno.routing.middlewares.base import Middleware, NextMiddleware
from maxo.kerno.types.update_context import UpdateContext
from maxo.kerno.types.updates.bot_added import BotAdded
from maxo.kerno.types.updates.bot_removed import BotRemoved
from maxo.kerno.types.updates.bot_started import BotStarted
from maxo.kerno.types.updates.chat_title_changed import ChatTitileChanged
from maxo.kerno.types.updates.message_callback import MessageCallback
from maxo.kerno.types.updates.message_chat_created import MessageChatCreated
from maxo.kerno.types.updates.message_created import MessageCreated
from maxo.kerno.types.updates.message_edited import MessageEdited
from maxo.kerno.types.updates.update import Update
from maxo.kerno.types.updates.user_added import UserAdded
from maxo.kerno.types.updates.user_removed import UserRemoved

UPDATE_CONTEXT_KEY: Final = "update_context"
UPDATE_USER_KEY: Final = "update_user"
UPDATE_CHAT_KEY: Final = "update_chat"


class UpdateContextMiddleware(Middleware[Update[Any]]):
    async def execute(
        self,
        update: Update[Any],
        ctx: Ctx[Update[Any]],
        next: NextMiddleware[Update[Any]],
    ) -> Any:
        update_context = ctx[UPDATE_CONTEXT_KEY] = self._resolve_update_context(update.update)

        if update_context.user is not None:
            ctx[UPDATE_USER_KEY] = update_context.user
        if update_context.chat is not None:
            ctx[UPDATE_CHAT_KEY] = update_context.chat

        return await next(ctx)

    def _resolve_update_context(self, update: Any) -> UpdateContext:
        chat = None
        chat_id = None
        user = None
        user_id = None

        if isinstance(update, (BotAdded, BotRemoved, BotStarted, ChatTitileChanged, UserAdded, UserRemoved)):
            chat_id = update.chat_id
            user = update.user
            user_id = user.user_id
        elif isinstance(update, MessageCallback):
            user = update.user
            user_id = user.user_id
            if update.message is not None and update.message.body is not None:
                chat_id = update.message.recipient.chat_id or update.message.recipient.user_id

        elif isinstance(update, MessageChatCreated):
            chat = update.chat
            chat_id = chat.chat_id
        elif isinstance(update, (MessageEdited, MessageCreated)):
            user = update.sender
            user_id = user.user_id

            if update.message is not None and update.message.body is not None:
                chat_id = update.message.recipient.chat_id or update.message.recipient.user_id

        return UpdateContext(
            chat=chat,
            chat_id=chat_id,
            user=user,
            user_id=user_id,
        )
