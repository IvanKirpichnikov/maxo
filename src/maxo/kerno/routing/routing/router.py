from abc import abstractmethod
from collections.abc import MutableMapping, MutableSequence
from typing import Any, Protocol, TypeVar

from maxo.kerno.routing.ctx import Ctx
from maxo.kerno.routing.routing.observer import UpdateObserver
from maxo.kerno.routing.sentinels import UNHANDLED
from maxo.kerno.types.updates.base import BaseUpdate
from maxo.kerno.types.updates.bot_added import BotAdded
from maxo.kerno.types.updates.bot_removed import BotRemoved
from maxo.kerno.types.updates.bot_started import BotStarted
from maxo.kerno.types.updates.chat_title_changed import ChatTitileChanged
from maxo.kerno.types.updates.dialog_cleared import DialogCleared
from maxo.kerno.types.updates.error import ErrorEvent
from maxo.kerno.types.updates.message_callback import MessageCallback
from maxo.kerno.types.updates.message_chat_created import MessageChatCreated
from maxo.kerno.types.updates.message_created import MessageCreated
from maxo.kerno.types.updates.message_edited import MessageEdited
from maxo.kerno.types.updates.message_removed import MessageRemoved
from maxo.kerno.types.updates.shutdown import Shutdown
from maxo.kerno.types.updates.startup import Startup
from maxo.kerno.types.updates.user_added import UserAdded
from maxo.kerno.types.updates.user_removed import UserRemoved

U = TypeVar("U", bound=BaseUpdate, covariant=True)


class RouterProtocol(Protocol):
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

    __slots__ = ()

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def parent_router(self) -> "RouterProtocol | None":
        raise NotImplementedError

    @property
    @abstractmethod
    def children_routers(self) -> MutableSequence["RouterProtocol"]:
        raise NotImplementedError

    @abstractmethod
    def include(self, *routers: "RouterProtocol") -> None:
        raise NotImplementedError

    @abstractmethod
    async def trigger_child(self, ctx: Ctx[U]) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def trigger(self, ctx: Ctx[U]) -> Any:
        raise NotImplementedError


class Router(RouterProtocol):
    __slots__ = (
        "_children_routers",
        "_name",
        "_parent_router",
        "bot_added",
        "bot_removed",
        "bot_started",
        "chat_title_changed",
        "dialog_cleared",
        "error",
        "message_callback",
        "message_chat_created",
        "message_created",
        "message_edited",
        "message_removed",
        "observers",
        "shutdown",
        "startup",
        "user_added",
        "user_removed",
    )

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
        self._children_routers: MutableSequence["RouterProtocol"] = []

    def __repr__(self) -> str:
        return f"<Router {self._name!r}>"

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent_router(self) -> RouterProtocol | None:
        return self._parent_router

    @property
    def children_routers(self) -> MutableSequence["RouterProtocol"]:
        return self._children_routers

    def include(self, *routers: RouterProtocol) -> None:
        self.children_routers.extend(routers)

    async def trigger_child(self, ctx: Ctx[U]) -> Any:
        for child_router in self.children_routers:
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
