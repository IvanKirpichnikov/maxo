from typing import Any, cast, final

from magic_filter import AttrDict, MagicFilter as OriginMagicFilter

from maxo.kerno.routing.ctx import Ctx
from maxo.kerno.routing.filters.base import Filter


@final
class MagicData(Filter[Any]):
    __slots__ = ("_magic_filter",)

    def __init__(self, magic_filter: OriginMagicFilter) -> None:
        self._magic_filter = magic_filter

    async def execute(self, update: Any, ctx: Ctx[Any]) -> bool:
        result = self._magic_filter.resolve(AttrDict({"update": ctx.update, **ctx.data}))
        return cast("bool", result)


@final
class MagicFilter(Filter[Any]):
    __slots__ = ("_magic_filter", "_save_key")

    def __init__(
        self,
        magic_filter: OriginMagicFilter,
        save_key: str | None = None,
    ) -> None:
        self._save_key = save_key
        self._magic_filter = magic_filter.cast(bool)

    async def execute(self, update: Any, ctx: Ctx[Any]) -> bool:
        result = self._magic_filter.resolve(ctx.update)
        if not result:
            return False

        if self._save_key is not None:
            ctx[self._save_key] = result

        return True
