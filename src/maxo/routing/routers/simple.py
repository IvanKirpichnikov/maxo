from collections.abc import Mapping, MutableMapping, MutableSequence
from typing import Any, TypeVar

from maxo.routing.ctx import Ctx
from maxo.routing.interfaces.observer import Observer
from maxo.routing.interfaces.router import Router, RouterState
from maxo.routing.middlewares.state import (
    EmptyMiddlewareManagerState,
    StartedMiddlewareManagerState,
)
from maxo.routing.observers.signal import SignalObserver
from maxo.routing.observers.state import EmptyObserverState, StartedObserverState
from maxo.routing.observers.update import UpdateObserver
from maxo.routing.routers.state import EmptyRouterState, StartedRouterState
from maxo.routing.sentinels import UNHANDLED
from maxo.routing.signals.exception import ExceptionEvent
from maxo.routing.signals.shutdown import AfterShutdown, BeforeShutdown
from maxo.routing.signals.startup import AfterStartup, BeforeStartup
from maxo.routing.updates.base import BaseUpdate
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
from maxo.routing.utils.get_default_name import get_router_default_name

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)


class SimpleRouter(Router):
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

    exception: SignalObserver[ExceptionEvent[Any]]
    before_startup: SignalObserver[BeforeStartup]
    after_startup: SignalObserver[AfterStartup]
    before_shutdown: SignalObserver[BeforeShutdown]
    after_shutdown: SignalObserver[AfterShutdown]

    _observers: MutableMapping[Any, Observer[Any, Any, Any]]

    __state: RouterState


    def __init__(self, name: str | None = None) -> None:
        self.bot_added = UpdateObserver()
        self.bot_removed = UpdateObserver()
        self.bot_started = UpdateObserver()
        self.chat_title_changed = UpdateObserver()
        self.message_callback = UpdateObserver()
        self.message_chat_created = UpdateObserver()
        self.message_created = UpdateObserver()
        self.message_edited = UpdateObserver()
        self.message_removed = UpdateObserver()
        self.user_added = UpdateObserver()
        self.user_removed = UpdateObserver()

        self.exception = SignalObserver()

        self.before_startup = SignalObserver()
        self.before_startup.handler(self._emit_before_startup_handler)

        self.after_startup = SignalObserver()

        self.before_shutdown = SignalObserver()
        self.before_shutdown.handler(self._emit_before_shutdown_handler)

        self.after_shutdown = SignalObserver()

        self._observers = {
            BotAdded: self.bot_added,
            BotRemoved: self.bot_removed,
            BotStarted: self.bot_started,
            ChatTitileChanged: self.chat_title_changed,
            MessageCallback: self.message_callback,
            MessageChatCreated: self.message_chat_created,
            MessageCreated: self.message_created,
            MessageEdited: self.message_edited,
            MessageRemoved: self.message_removed,
            UserAdded: self.user_added,
            UserRemoved: self.user_removed,
            ExceptionEvent: self.exception,
            BeforeStartup: self.before_startup,
            AfterStartup: self.after_startup,
            BeforeShutdown: self.before_shutdown,
            AfterShutdown: self.after_shutdown,
        }

        if name is None:
            name = get_router_default_name()

        self._name = name
        self._children_routers: MutableSequence[Router] = []
        self.__state = EmptyRouterState()

    def __repr__(self) -> str:
        return f"<Router {self._name!r}>"

    @property
    def _state(self) -> RouterState:
        return self.__state

    @_state.setter
    def _state(self, value: RouterState) -> None:
        self.__state = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def observers(self) -> Mapping[Any, Observer[Any, Any, Any]]:
        return self._observers

    @property
    def children_routers(self) -> MutableSequence[Router]:
        return self._children_routers

    def include(self, *routers: Router) -> None:
        self._state.ensure_include()
        self.children_routers.extend(routers)

    async def trigger_child(self, ctx: Ctx[_UpdateT]) -> Any:
        for child_router in self.children_routers:
            return await child_router.trigger(ctx)
        return UNHANDLED

    async def trigger(self, ctx: Ctx[_UpdateT]) -> Any:
        observer = self.observers.get(ctx.update_tp)
        if observer is None:
            return await self.trigger_child(ctx)

        observer_filter_result = await observer.execute_filter(ctx)
        if not observer_filter_result:
            return await self.trigger_child(ctx)

        chain_middlewares = observer.middleware.outer._make_chain(observer.handler_lookup)
        result = await chain_middlewares(ctx)
        if result is UNHANDLED:
            return await self.trigger_child(ctx)
        else:
            return result

    async def _emit_before_startup_handler(self, ctx: Ctx[BeforeStartup]) -> None:
        self._state = StartedRouterState()

        for observer in self.observers.values():
            observer._state = StartedObserverState()

            observer.middleware.inner._state = StartedMiddlewareManagerState()
            observer.middleware.outer._state = StartedMiddlewareManagerState()

    async def _emit_before_shutdown_handler(self, ctx: Ctx[BeforeShutdown]) -> None:
        self._state = EmptyRouterState()

        for observer in self.observers.values():
            observer._state = EmptyObserverState()

            observer.middleware.inner._state = EmptyMiddlewareManagerState()
            observer.middleware.outer._state = EmptyMiddlewareManagerState()
