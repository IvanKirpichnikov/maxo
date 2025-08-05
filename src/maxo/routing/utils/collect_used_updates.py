from typing import Sequence, overload

from maxo.routing.interfaces.router import Router
from maxo.routing.updates.base import MaxUpdate
from maxo.types.enums.update_type import UpdateType


def _collect_used_updates_type(router: Router) -> set[UpdateType]:
    used_updates = set()
    for update_tp, observer in router.observers.items():
        if (
            issubclass(update_tp, MaxUpdate)
            and observer.handlers
            and update_tp.type is not None
        ):
            used_updates.add(update_tp.type)

    return used_updates


@overload
def collect_used_updates(
    router: Router,
) -> Sequence[str]: ...


@overload
def collect_used_updates(
    router: Router,
    used_updates: set[UpdateType],
) -> Sequence[str]: ...


def collect_used_updates(
    router: Router,
    used_updates: set[UpdateType] | None = None,
) -> Sequence[str]:
    if used_updates is None:
        used_updates = set()

    used_updates |= _collect_used_updates_type(router)

    for children_router in router.children_routers:
        collect_used_updates(children_router, used_updates)

    return tuple(used_updates)
