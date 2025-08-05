from inspect import isclass
from typing import Any

from maxo.alta.state_system.state import State, StatesGroup, any_state
from maxo.routing.ctx import Ctx
from maxo.routing.filters.base import BaseFilter


class StateFilter(BaseFilter[Any]):
    __slots__ = ("_states",)

    def __init__(
        self,
        *states: State | StatesGroup | type[StatesGroup] | None | str,
    ) -> None:
        self._states = states

    async def execute(self, update: Any, ctx: Ctx[Any]) -> bool:
        raw_state = ctx.raw_state

        for state in self._states:
            if (isinstance(state, str) or state is None) and (state in (any_state, raw_state)):
                return True
            if isinstance(state, State) and raw_state == state:
                return True
            if isclass(state) and issubclass(state, StatesGroup) and raw_state in StatesGroup:
                return True

        return False
