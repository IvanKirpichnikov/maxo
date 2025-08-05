from typing import Any, final

try:
    from magic_filter import AttrDict, MagicFilter as OriginMagicFilter
except ImportError as e:
    e.add_note(" * Please run `pip install maxo[magic_filter]`")
    raise

from maxo.routing.ctx import Ctx
from maxo.routing.filters.base import BaseFilter


@final
class MagicData(BaseFilter[Any]):
    __slots__ = ("_magic_filter",)

    def __init__(self, magic_filter: OriginMagicFilter) -> None:
        self._magic_filter = magic_filter

    async def execute(self, update: Any, ctx: Ctx[Any]) -> bool:
        result = self._magic_filter.resolve(AttrDict({"update": update, **ctx.raw_data}))
        return bool(result)


@final
class MagicFilter(BaseFilter[Any]):
    __slots__ = ("_magic_filter", "_result_key")

    def __init__(
        self,
        magic_filter: OriginMagicFilter,
        result_key: str | None = None,
    ) -> None:
        self._result_key = result_key
        self._magic_filter = magic_filter.cast(bool)

    async def execute(self, update: Any, ctx: Ctx[Any]) -> bool:
        result = self._magic_filter.resolve(update)
        if not result:
            return False

        if self._result_key is not None:
            setattr(ctx.state, self._result_key, result)

        return True
