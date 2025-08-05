from typing import TYPE_CHECKING, Any, Generic, TypeVar

from maxo.routing.ctx import Ctx
from maxo.routing.handlers.signal import SignalHandler, SignalHandlerFn
from maxo.routing.interfaces.filter import Filter
from maxo.routing.observers.base import BaseObserver
from maxo.routing.sentinels import UNHANDLED
from maxo.routing.signals.base import BaseSignal

_SignalT = TypeVar("_SignalT", bound=BaseSignal)
_ReturnT_co = TypeVar("_ReturnT_co", covariant=True)


class SignalObserver(
    BaseObserver[
        _SignalT,
        SignalHandler[_SignalT, Any],
        SignalHandlerFn[_SignalT, Any],
    ],
    Generic[_SignalT],
):
    def handler(
        self,
        handler_fn: SignalHandlerFn[_SignalT, Any],
        filter: Filter[_SignalT] | None = None,
    ) -> SignalHandlerFn[_SignalT, Any]:
        self._state.ensure_add_handler()

        self._handlers.append(SignalHandler(handler_fn, filter))

        return handler_fn


    async def handler_lookup(self, ctx: Ctx[_SignalT]) -> Any:
        result = UNHANDLED

        for handler in self._handlers:
            if await handler.execute_filter(ctx):
                result = await self.execute_handler(ctx, handler)

        return result

    if TYPE_CHECKING:

        async def execute_handler(
            self,
            ctx: Ctx[_SignalT],
            handler: SignalHandler[_SignalT, _ReturnT_co],
        ) -> _ReturnT_co: ...
