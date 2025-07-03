from collections import defaultdict
from copy import copy
from typing import Any, MutableMapping, MutableSequence, Sequence, overload

from maxo.errors.routing import CycleRoutersError
from maxo.kerno.routing.middlewares.base import Middleware
from maxo.kerno.routing.routing.router import RouterProtocol
from maxo.kerno.types.enums.update_type import UpdateType
from maxo.kerno.types.updates.base import BaseUpdate
from maxo.kerno.types.updates.update import Update


def resolve_middlewares(
    router: RouterProtocol,
    middlewares_map: MutableMapping[type[BaseUpdate], MutableSequence[Middleware[Any]]],
) -> None:
    update_observer = router.observers[Update]
    for update_tp, observer in router.observers.items():
        middlewares = [
            *middlewares_map[update_tp],
            *update_observer.inner_middleware.middlewares,
        ]
        observer.inner_middleware(*middlewares)
        middlewares_map[update_tp] = copy(middlewares)


def collect_used_updates_type(router: RouterProtocol) -> set[UpdateType]:
    used_updates = set()
    for update_tp, observer in router.observers.items():
        if observer.handlers:
            type = getattr(update_tp, "type", None)
            if type is not None:
                used_updates.add(type)

    return used_updates


@overload
def walking_router_graph(
    router: RouterProtocol,
) -> Sequence[str]: ...


@overload
def walking_router_graph(
    router: RouterProtocol,
    used_updates: set[UpdateType],
    visited_routers: MutableSequence[RouterProtocol],
    middlewares_map: MutableMapping[type[BaseUpdate], MutableSequence[Middleware[Any]]],
) -> Sequence[str]: ...


def walking_router_graph(
    router: RouterProtocol,
    used_updates: set[UpdateType] | None = None,
    visited_routers: MutableSequence[RouterProtocol] | None = None,
    middlewares_map: MutableMapping[type[BaseUpdate], MutableSequence[Middleware[Any]]] | None = None,
) -> Sequence[str]:
    if used_updates is None:
        used_updates = set()

    if visited_routers is None:
        visited_routers = []

    if middlewares_map is None:
        middlewares_map = defaultdict(list)

    visited_routers.append(router)
    resolve_middlewares(router, middlewares_map)
    used_updates |= collect_used_updates_type(router)

    for children_router in router.children_routers:
        if children_router in visited_routers:
            raise CycleRoutersError(visited_routers)

        walking_router_graph(children_router, used_updates, copy(visited_routers), middlewares_map)

    return tuple(used_updates)
