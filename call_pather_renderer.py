from abc import abstractmethod
from contextlib import AbstractContextManager
from dataclasses import dataclass
from functools import partial, wraps
from types import TracebackType
from typing import Any, Callable, Iterable, Protocol, Sequence, TypeAlias


@dataclass
class CallPathRendererConfig:
    right_pointing: str = "›"
    left_pointing: str = "‹"

    start_path: str = "×"
    end_path: str = "×"

    connector: str = "│"
    transition_path: str = "├──▷"

    continue_call_path: str = "╰┬─▷"
    continue_returned_call_path: str = "╭┴─▷"


@dataclass
class CallPathNode:
    obj: Any
    type: str
    context: dict[str, Any]
    error: BaseException | None


class CallPathRenderer(Protocol):
    @abstractmethod
    def render(
        self,
        call_path: Sequence[CallPathNode],
        returned_call_path: Sequence[CallPathNode],
    ) -> str:
        raise NotImplementedError


class DefaultCallPathRenderer(CallPathRenderer):
    def __init__(self, config: CallPathRendererConfig) -> None:
        self._config = config

    def render(
        self,
        call_path: Sequence[CallPathNode],
        returned_call_path: Sequence[CallPathNode],
    ) -> str:
        if not call_path:
            return ""

        has_returned_call_path = bool(returned_call_path)

        rendered_call_path = self._render_call_path(call_path, has_returned_call_path)

        if not has_returned_call_path:
            return "\n".join(
                rendered_call_path,
            )

        return "\n".join(
            (
                *rendered_call_path,
                self._render_node_connector(len(returned_call_path) - 1),
                *self._render_returned_call_path(returned_call_path),
            ),
        )

    def _render_call_path(
        self,
        call_path: Sequence[CallPathNode],
        has_returned_call_path: bool,
    ) -> Iterable[str]:
        result = []
        config = self._config

        last_call_path_node_index = len(call_path) - 1
        for index, node in enumerate(call_path):
            if index == 0:
                context_path = config.start_path
                location_path = config.continue_call_path
            elif index == last_call_path_node_index:
                context_path = config.connector
                location_path = (
                    config.transition_path if has_returned_call_path else config.continue_call_path
                )
            else:
                context_path = config.connector
                location_path = config.continue_call_path

            result.append(
                self._render_node(
                    indent=index,
                    node=node,
                    context_path=context_path,
                    location_path=location_path,
                    returned_path=False,
                )
            )

        return result

    def _render_returned_call_path(
        self,
        returned_call_path: Sequence[CallPathNode],
    ) -> Iterable[str]:
        result = []

        returned_call_path_len = len(returned_call_path)
        for index, node in enumerate(returned_call_path, start=1):
            if index == 1:
                context_path = self._config.connector
                location_path = self._config.transition_path
            elif index == returned_call_path_len:
                context_path = self._config.end_path
                location_path = self._config.continue_returned_call_path
            else:
                context_path = self._config.connector
                location_path = self._config.continue_returned_call_path

            result.append(
                self._render_node(
                    indent=max(0, returned_call_path_len - index),
                    node=node,
                    context_path=context_path,
                    location_path=location_path,
                    returned_path=True,
                )
            )

        return result

    def _render_node_connector(self, indent: int) -> str:
        node_connector = self._render_indent(indent) + self._config.connector
        return "\n".join(node_connector for _ in range(2))

    def _render_node(
        self,
        indent: int,
        node: CallPathNode,
        location_path: str,
        context_path: str,
        *,
        returned_path: bool,
    ) -> str:
        row = [
            self._render_node_context(indent, node, context_path),
            self._render_node_location(indent, node, location_path),
        ]
        if node.error is not None:
            row.insert(1, self._render_node_error(indent, node))

        return "\n".join(reversed(row) if returned_path else row)

    def _render_node_context(self, indent: int, node: CallPathNode, path: str) -> str:
        return (
            self._render_indent(indent) + path + self._render_indent(5) + f"Context: {node.context}"
        )

    def _render_node_location(self, indent: int, node: CallPathNode, path: str) -> str:
        obj_module_and_name = f"{node.obj.__module__}:{node.obj.__name__}"
        location = (
            node.type
            + " "
            + self._config.left_pointing
            + obj_module_and_name
            + self._config.right_pointing
        )

        return self._render_indent(indent) + path + self._render_indent(2) + f"Location: {location}"

    def _render_node_error(self, indent: int, node: CallPathNode) -> str:
        return (
            self._render_indent(indent)
            + self._config.connector
            + self._render_indent(5)
            + f"Error: {node.error!r}"
        )

    def _render_indent(self, indent: int) -> str:
        return indent * " "


class CallPathNodeCollector:
    def __init__(self) -> None:
        self._call_path: list[CallPathNode] = []
        self._returned_call_path: list[CallPathNode] = []

    @property
    def call_path(self) -> Sequence[CallPathNode]:
        return self._call_path

    @property
    def returned_call_path(self) -> Sequence[CallPathNode]:
        return self._returned_call_path

    def __call__(
        self,
        obj: Any,
        type: str,
        context: dict[str, Any],
    ) -> "CallPathNodeCollectorWrapper":
        return CallPathNodeCollectorWrapper(
            collector=self,
            obj=obj,
            type=type,
            context=context,
        )

    def _add(
        self,
        obj: Any,
        type: str,
        context: dict[str, Any],
        *,
        returned: bool = False,
        error: BaseException | None = None,
    ) -> None:
        call_path = self._returned_call_path if returned else self._call_path

        call_path.append(
            CallPathNode(
                obj=obj,
                type=type,
                context=context,
                error=error,
            )
        )


class CallPathNodeCollectorWrapper(AbstractContextManager[None, None]):
    def __init__(
        self,
        collector: CallPathNodeCollector,
        obj: Any,
        type: str,
        context: dict[str, Any],
    ) -> None:
        self._collector = collector
        self._obj = obj
        self._type = type
        self._context = context

    def __enter__(self) -> None:
        self._collector._add(
            self._obj,
            type=self._type,
            context=self._context,
        )

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._collector._add(
            self._obj,
            type=self._type,
            context=self._context,
            error=exc_value,
            returned=True,
        )


def call_path_collector_dec(type: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            chain: CallPathNodeCollector = args[-1]
            with chain(func, type, {"my_data": "a"}):
                return func(*args, **kwargs)

        return wrapper

    return decorator


NextMiddleware: TypeAlias = Callable[["CallPathNodeCollector"], Any]


def error_middleware(
    next: NextMiddleware,
    call_path_node_collector: CallPathNodeCollector,
) -> Any:
    next(call_path_node_collector)


def di_middleware(
    next: NextMiddleware,
    call_path_node_collector: CallPathNodeCollector,
) -> Any:
    try:
        next(call_path_node_collector)
    except Exception as e:
        raise RuntimeError("Другая аошибка, которая после другой ашибки") from e


def upsert_user_middleware(
    next: NextMiddleware,
    call_path_node_collector: CallPathNodeCollector,
) -> Any:
    # raise ValueError
    next(call_path_node_collector)


@call_path_collector_dec("Handler")
def start_handler(call_path_node_collector: CallPathNodeCollector) -> None:
    raise ValueError("Ашибка")
    # pass


def _last_middleware(call_path_node_collector: CallPathNodeCollector) -> Any:
    return start_handler(call_path_node_collector)


_mid = _last_middleware
middlewares = [error_middleware, di_middleware, upsert_user_middleware]
for midd in reversed(middlewares):
    _mid = partial(call_path_collector_dec("Middleware")(midd), _mid)


collector = CallPathNodeCollector()
# renderer = DefaultCallPathRenderer(
#     CallPathRendererConfig(
#         right_pointing=">",
#         left_pointing="<",
#         start_path="+",
#         end_path="+",
#         connector="|",
#         transition_path="|-->",
#         continue_call_path="|-->",
#         continue_returned_call_path="|-->",
#     )
# )

renderer = DefaultCallPathRenderer(CallPathRendererConfig())

try:
    _mid(collector)
except Exception as e:
    e.add_note(
        renderer.render(
            collector.call_path,
            collector.returned_call_path,
        )
    )
    raise
