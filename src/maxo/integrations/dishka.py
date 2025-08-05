from typing import Any, Callable, Concatenate, ParamSpec, TypeVar, overload

from dishka import AsyncContainer

from maxo.routing.handlers.signal import SignalHandlerFn
from maxo.routing.handlers.update import UpdateHandlerFn
from maxo.routing.interfaces.middleware import Middleware, NextMiddleware
from maxo.routing.signals.base import BaseSignal
from maxo.routing.signals.update import Update

try:
    from dishka import Provider, Scope, from_context
    from dishka.integrations.base import wrap_injection
except ImportError as e:
    e.add_note(" * Please run `pip install maxo[dishka]`")
    raise

from maxo.alta.dispatcher import Dispatcher
from maxo.alta.state_system.manager import StateManager
from maxo.alta.state_system.storages.base import RawState, Storage
from maxo.bot.bot import Bot
from maxo.routing.ctx import Ctx
from maxo.routing.updates.base import BaseUpdate
from maxo.types.update_context import UpdateContext

_ReturnT = TypeVar("_ReturnT")
_ParamsP = ParamSpec("_ParamsP")
_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)
_SignalT = TypeVar("_SignalT", bound=BaseSignal)

_SignalHandlerFn = Callable[Concatenate[Ctx[_SignalT], _ParamsP], _ReturnT]
_UpdateHandlerFn = Callable[Concatenate[_UpdateT, Ctx[_UpdateT], _ParamsP], _ReturnT]


@overload
def inject(
    func: _SignalHandlerFn[_SignalT, _ParamsP, _ReturnT],
) -> SignalHandlerFn[_SignalT, _ReturnT]:
    ...

@overload
def inject(
    func: _UpdateHandlerFn[_UpdateT, _ParamsP, _ReturnT],
) -> UpdateHandlerFn[_UpdateT, _ReturnT]:
    ...

def inject(func: Any) ->  Any:
    return wrap_injection(
        func=func,
        is_async=True,
        container_getter=lambda args, kwargs: kwargs["ctx"].data.dishka_container,
    )

def setup_dishka(
    dispatcher: Dispatcher,
    container: AsyncContainer,
    auto_inject: bool,
    extra_context: dict[Any, Any] | None = None,
) -> None:
    dispatcher.update.middleware.outer(
        DishkaMiddleware(container, extra_context),
    )


class DishkaMiddleware(Middleware[Update[Any]]):
    __slots__ = ("_container", "_extra_context")

    def __init__(
        self,
        container: AsyncContainer,
        extra_context: dict[Any, Any] | None = None
    ) -> None:
        self._container = container
        self._extra_context = extra_context or {}

    async def execute(
        self,
        update: Update[Any],
        ctx: Ctx[Update[Any]],
        next: NextMiddleware[Update[Any]],
    ) -> Any:
        async with self._container(
            {
                Update[Any]: update,
                Update[type(update.update)]: update,  # type: ignore[misc]
                Ctx[Update[Any], Any]: ctx,
                Ctx[Update[type(update.update)], Any]: ctx,  # type: ignore[misc]
            } | self._extra_context,
        ) as container:
            ctx.dishka_container = container
            return await next(ctx)


class MaxoProvider(Provider):
    scope = Scope.REQUEST

    context = (
        from_context(Bot)
        + from_context(Dispatcher)
        + from_context(UpdateContext)
        + from_context(Storage)
        + from_context(StateManager)
        + from_context(RawState)
        + from_context(Update[Any])
        + from_context(Update[_UpdateT])
        + from_context(Update[Any])
        + from_context(Ctx[Update[Any], Any])
        + from_context(Ctx[Update[_UpdateT], Any])
    )
