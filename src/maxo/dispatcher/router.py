from collections.abc import MutableMapping, MutableSequence
from typing import Any, TypeVar

from maxo.dispatcher.ctx import Ctx
from maxo.dispatcher.observer import UpdateObserver
from maxo.dispatcher.sentinels import UNHANDLED
from maxo.types.updates.base import BaseUpdate
from maxo.types.updates.bot_added import BotAdded
from maxo.types.updates.bot_removed import BotRemoved
from maxo.types.updates.bot_started import BotStarted
from maxo.types.updates.chat_title_changed import ChatTitileChanged
from maxo.types.updates.dialog_cleared import DialogCleared
from maxo.types.updates.error import ErrorEvent
from maxo.types.updates.message_callback import MessageCallback
from maxo.types.updates.message_chat_created import MessageChatCreated
from maxo.types.updates.message_created import MessageCreated
from maxo.types.updates.message_edited import MessageEdited
from maxo.types.updates.message_removed import MessageRemoved
from maxo.types.updates.shutdown import Shutdown
from maxo.types.updates.startup import Startup
from maxo.types.updates.user_added import UserAdded
from maxo.types.updates.user_removed import UserRemoved

U = TypeVar("U", bound=BaseUpdate)


class Router:
    observers: MutableMapping[type[Any], UpdateObserver[Any]]

    bot_added: UpdateObserver[BotAdded]
    bot_removed: UpdateObserver[BotRemoved]
    bot_started: UpdateObserver[BotStarted]
    chat_title_changed: UpdateObserver[ChatTitileChanged]
    message_callback: UpdateObserver[MessageCallback]
    message_chat_created: UpdateObserver[MessageChatCreated]
    message_created: UpdateObserver[MessageCreated]
    message_edited: UpdateObserver[MessageEdited]
    message_removed: UpdateObserver[MessageRemoved]
    user_added: UpdateObserver[UserAdded]
    user_removed: UpdateObserver[UserRemoved]
    dialog_cleared: UpdateObserver[DialogCleared]
    startup: UpdateObserver[Startup]
    shutdown: UpdateObserver[Shutdown]
    error: UpdateObserver[ErrorEvent[Any]]

    _parent_router: "Router | None"
    _children_routers: MutableSequence["Router"]

    def __init__(self, name: str) -> None:
        self.observers = {
            BotAdded: UpdateObserver(),
            BotRemoved: UpdateObserver(),
            BotStarted: UpdateObserver(),
            ChatTitileChanged: UpdateObserver(),
            MessageCallback: UpdateObserver(),
            MessageChatCreated: UpdateObserver(),
            MessageCreated: UpdateObserver(),
            MessageEdited: UpdateObserver(),
            MessageRemoved: UpdateObserver(),
            Shutdown: UpdateObserver(),
            Startup: UpdateObserver(),
            UserAdded: UpdateObserver(),
            UserRemoved: UpdateObserver(),
            ErrorEvent: UpdateObserver(),
            DialogCleared: UpdateObserver(),
        }

        self.bot_added = self.observers[BotAdded]
        self.bot_removed = self.observers[BotRemoved]
        self.bot_started = self.observers[BotStarted]
        self.chat_title_changed = self.observers[ChatTitileChanged]
        self.message_callback = self.observers[MessageCallback]
        self.message_chat_created = self.observers[MessageChatCreated]
        self.message_created = self.observers[MessageCreated]
        self.message_edited = self.observers[MessageEdited]
        self.message_removed = self.observers[MessageRemoved]
        self.user_added = self.observers[UserAdded]
        self.user_removed = self.observers[UserRemoved]
        self.dialog_cleared = self.observers[DialogCleared]
        self.startup = self.observers[Startup]
        self.shutdown = self.observers[Shutdown]
        self.error = self.observers[ErrorEvent]

        self._name = name

        self._parent_router = None
        self._children_routers = []

    def __repr__(self) -> str:
        return f"<Router {self._name!r}>"

    def include(self, router: "Router") -> None:
        self._children_routers.append(router)

    async def trigger_child(self, ctx: Ctx[U]) -> Any:
        for child_router in self._children_routers:
            return await child_router.trigger(ctx)
        return UNHANDLED

    async def trigger(self, ctx: Ctx[U]) -> Any:
        observer = self.observers.get(ctx.update_tp)
        if observer is not None:
            chain_middlewares = observer.outer_middleware.make_chain(observer.search_handler)
            result = await chain_middlewares(ctx)
            if result is UNHANDLED:
                return await self.trigger_child(ctx)
            else:
                return result
        else:
            return await self.trigger_child(ctx)
