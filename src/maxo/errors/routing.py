from typing import TYPE_CHECKING, Sequence

from maxo.errors.base import MaxoError, maxo_error

if TYPE_CHECKING:
    from maxo.routing.interfaces.router import Router


@maxo_error
class CycleRoutersError(MaxoError):
    routers: Sequence["Router"]

    def __str__(self) -> str:
        details = self._render_details()
        return f"Cycle routers detected.\n{details}"

    def _render_details(self) -> str:
        routers = self.routers

        if len(routers) == 1:
            return f"⥁ {routers[0]}"

        details = "╭─>─╮\n"
        start = True
        for router in routers:
            if not start:
                details += "│   ▼\n"
            details += f"│ {router}\n"
            start = False

        details += "╰─<─╯"

        return details
