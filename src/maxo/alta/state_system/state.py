from collections.abc import Sequence
from typing import Any, Final


class State:
    _name: str | None
    _group: "type[StatesGroup] | None"

    __slots__ = ("_group", "_name")

    def __init__(self, name: str | None = None) -> None:
        self._name = name
        self._group = None

    @property
    def name(self) -> str:
        if self._name is None:
            raise RuntimeError
        return self._name

    @property
    def group(self) -> "type[StatesGroup] | None":
        return self._group

    @property
    def state(self) -> str:
        if self._group is None:
            return self.name
        return f"{self._group.__name__}.{self.name}"

    def __set_name__(
        self,
        owner: "type[StatesGroup]",
        name: str,
    ) -> None:
        self._name = name
        self._group = owner

    def __repr__(self) -> str:
        return f"<State {self.state}>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, State | str):
            return NotImplemented

        if self.state == "*":
            return True

        raw_state = other.state if isinstance(other, State) else other

        if raw_state == "*":
            return True

        return raw_state == self.state


class StatesGroupMetaClass(type):
    __states__: Sequence[State]
    __raw_states__: Sequence[str]

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        /,
        **kwargs: Any,
    ) -> Any:
        class_ = super().__new__(cls, name, bases, namespace, **kwargs)

        states = [value for value in namespace.values() if isinstance(value, State)]

        class_.__states__ = tuple(states)
        class_.__raw_states__ = tuple(x.state for x in states)

        return class_

    def __repr__(cls) -> str:
        return f"StatesGroup{cls.__states__}"

    def __contains__(cls, other: Any) -> bool:
        if not isinstance(other, State | str):
            return False

        state = other.state if isinstance(other, State) else other
        if state == "*":
            return True

        return state in cls.__raw_states__


class StatesGroup(metaclass=StatesGroupMetaClass):
    __slots__ = ("__raw_states__", "__states__")


any_state: Final = State("*")
