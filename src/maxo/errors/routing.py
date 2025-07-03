from typing import Sequence

from maxo.errors.base import MaxoError, error
from maxo.kerno.routing.routing.router import RouterProtocol


@error
class CycleRoutersError(MaxoError):
    routers: Sequence[RouterProtocol]

    def _generate_details(self) -> str:
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

    def __str__(self) -> str:
        details = self._generate_details()
        return f"Cycle routers detected.\n{details}"
