from maxo.types.base import MaxoType


class UpdateContext(MaxoType):
    chat_id: int | None = None
    user_id: int | None = None
