from copy import copy
from typing import MutableSequence, overload

from maxo.errors.routing import CycleRoutersError
from maxo.routing.interfaces.router import Router


@overload
def validate_router_graph(
    router: Router,
) -> None: ...


@overload
def validate_router_graph(
    router: Router,
    visited_routers: MutableSequence[Router],
) -> None: ...


def validate_router_graph(
    router: Router,
    visited_routers: MutableSequence[Router] | None = None,
) -> None:
    if visited_routers is None:
        visited_routers = []

    visited_routers.append(router)

    for children_router in router.children_routers:
        if children_router in visited_routers:
            raise CycleRoutersError(visited_routers)

        validate_router_graph(children_router, copy(visited_routers))
