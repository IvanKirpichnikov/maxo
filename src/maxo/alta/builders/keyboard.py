from collections.abc import (
    Generator,
    Iterable,
    MutableSequence,
    Sequence,
)
from copy import deepcopy
from itertools import chain, cycle
from typing import ClassVar, TypeVar

from typing_extensions import Self

from maxo.kerno.types.enums.intent import IntentType
from maxo.kerno.types.types.keyboard_buttons import (
    CallbackKeyboardButton,
    ChatKeyboardButton,
    KeyboardButtons,
    LinkKeyboardButton,
    RequestContactKeyboardButton,
    RequestGeoLocationKeyboardButton,
)
from maxo.omit import Omittable, Omitted

T = TypeVar("T")


def repeat_last(items: Iterable[T]) -> Generator[T, None, None]:
    items_iter = iter(items)

    try:
        value = next(items_iter)
    except StopIteration:
        return

    yield value

    finished = False
    while True:
        if not finished:
            try:
                value = next(items_iter)
            except StopIteration:
                finished = True
        yield value


class KeyboardValidator:
    max_width: ClassVar[int] = 7
    min_width: ClassVar[int] = 1
    max_buttons: ClassVar[int] = 210

    def validate_keyboard(self, markup: Sequence[Sequence[KeyboardButtons]]) -> bool:
        count = 0
        for row in markup:
            self.validate_row(row)
            count += len(row)
        if count > self.max_buttons:
            raise ValueError(f"Too much buttons detected Max allowed count - {self.max_buttons}")
        return True

    def validate_row(self, row: Sequence[KeyboardButtons]) -> None:
        if len(row) > self.max_width:
            raise ValueError(f"Row {row!r} is too long (max width: {self.max_width})")

    def validate_size(self, size: int) -> int:
        if size not in range(self.min_width, self.max_width + 1):
            raise ValueError(f"Row size {size} is not allowed, range: [{self.min_width}, {self.max_width}]")
        return size


class KeyboardBuilder:
    _keyboard: MutableSequence[MutableSequence[KeyboardButtons]]

    def __init__(
        self,
        keyboard: MutableSequence[MutableSequence[KeyboardButtons]] | None = None,
    ) -> None:
        validator = KeyboardValidator()

        if keyboard:
            validator.validate_keyboard(keyboard)
        else:
            keyboard = []

        self._keyboard = keyboard
        self._validator = validator

    def add_callback(
        self,
        text: str,
        payload: str,
        intent: IntentType = IntentType.DEFAULT,
    ) -> Self:
        self.add(
            CallbackKeyboardButton(
                text=text,
                intent=intent,
                payload=payload,
            )
        )
        return self

    def add_chat(
        self,
        text: str,
        title: str,
        description: Omittable[str | None] = Omitted(),
        start_payload: Omittable[str | None] = Omitted(),
        uuid: Omittable[int | None] = Omitted(),
    ) -> Self:
        self.add(
            ChatKeyboardButton(
                text=text,
                chat_title=title,
                chat_description=description,
                start_payload=start_payload,
                uuid=uuid,
            )
        )
        return self

    def add_link(self, text: str, url: str) -> Self:
        self.add(
            LinkKeyboardButton(
                text=text,
                url=url,
            )
        )
        return self

    def add_request_contact(self, text: str) -> Self:
        self.add(
            RequestContactKeyboardButton(
                text=text,
            )
        )
        return self

    def add_request_geo_location(self, text: str, quick: Omittable[bool] = Omitted()) -> Self:
        self.add(
            RequestGeoLocationKeyboardButton(
                text=text,
                quick=quick,
            )
        )
        return self

    @property
    def buttons(self) -> Generator[KeyboardButtons, None, None]:
        yield from chain.from_iterable(self.build())

    def build(self) -> MutableSequence[MutableSequence[KeyboardButtons]]:
        return deepcopy(self._keyboard)

    def add(self, *buttons: KeyboardButtons) -> Self:
        self._validator.validate_row(buttons)
        keyboard = self.build()

        if keyboard and len(keyboard[-1]) < self._validator.max_width:
            last_row = keyboard[-1]
            pos = self._validator.max_width - len(last_row)
            head, buttons = buttons[:pos], buttons[pos:]
            last_row.extend(head)

        if self._validator.max_width > 0:
            while buttons:
                row, buttons = (
                    buttons[: self._validator.max_width],
                    buttons[self._validator.max_width :],
                )
                keyboard.append(list(row))
        else:
            keyboard.append(list(buttons))

        self._keyboard = keyboard
        return self

    def row(self, *buttons: KeyboardButtons, width: int | None = None) -> Self:
        if width is None:
            width = self._validator.max_width

        self._validator.validate_size(width)
        self._validator.validate_row(buttons)
        self._keyboard.extend(list(buttons[pos : pos + width]) for pos in range(0, len(buttons), width))
        return self

    def adjust(self, *sizes: int, repeat: bool = False) -> Self:
        if not sizes:
            sizes = (self._validator.max_width,)

        validated_sizes = map(self._validator.validate_size, sizes)
        sizes_iter = cycle(validated_sizes) if repeat else repeat_last(validated_sizes)
        size = next(sizes_iter)

        keyboard = []
        row: MutableSequence[KeyboardButtons] = []
        for button in self.buttons:
            if len(row) >= size:
                keyboard.append(row)
                size = next(sizes_iter)
                row = []
            row.append(button)
        if row:
            keyboard.append(row)

        self._keyboard = keyboard

        return self

    def attach(self, builder: "KeyboardBuilder") -> "KeyboardBuilder":
        self._keyboard.extend(builder.build())
        return self
