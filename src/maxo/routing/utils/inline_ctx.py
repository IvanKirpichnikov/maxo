from functools import wraps
from inspect import signature
from typing import Any, Callable, Concatenate, ParamSpec, TypeVar, overload

from maxo.routing.ctx import Ctx
from maxo.routing.handlers.signal import SignalHandlerFn
from maxo.routing.handlers.update import UpdateHandlerFn
from maxo.routing.signals.base import BaseSignal
from maxo.routing.updates.base import BaseUpdate

_ReturnT = TypeVar("_ReturnT")
_ParamsT = ParamSpec("_ParamsT")
_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)
_SignalT = TypeVar("_SignalT", bound=BaseSignal)


_SignalHandlerFn = Callable[Concatenate[Ctx[_SignalT], _ParamsT], _ReturnT]
_UpdateHandlerFn = Callable[Concatenate[_UpdateT, Ctx[_UpdateT], _ParamsT], _ReturnT]


@overload
def inline_ctx(
    func: _SignalHandlerFn[_SignalT, _ParamsT, _ReturnT],
) -> SignalHandlerFn[_SignalT, _ReturnT]:
    ...

@overload
def inline_ctx(
    func: _UpdateHandlerFn[_UpdateT, _ParamsT, _ReturnT],
) -> UpdateHandlerFn[_UpdateT, _ReturnT]:
    ...

# TODO: maybe make code generetor?
# TODO: add support custom handlers
def inline_ctx(func: Any) -> Any:
    func_signature = signature(func)
    parameters = list(func_signature.parameters.values())

    is_update_handler_fn = parameters[0].name == "update"

    if is_update_handler_fn:
        inline_paramaters = [parameter.name for parameter in parameters[2:]]
    else:
        inline_paramaters = [parameter.name for parameter in parameters[1:]]

    @wraps(func)
    async def handler(*args: Any, **kwargs: Any) -> Any:
        ctx: Ctx[Any] = kwargs["ctx"]

        inline_kwargs = {
            inline_paramater: getattr(ctx, inline_paramater)
            for inline_paramater in inline_paramaters
        }
        return await func(*args, **kwargs, **inline_kwargs)
    return handler
