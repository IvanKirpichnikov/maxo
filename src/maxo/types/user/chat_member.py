from collections.abc import Sequence
from datetime import datetime

from maxo.enums.chat_admin_merpission_type import ChatAdminPermissionType
from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class ChatMember(MaxoType):
    user_id: int
    first_name: str
    last_name: Omittable[str] = Omitted()
    username: str | None = None
    is_bot: bool
    last_activity_time: datetime
    description: Omittable[str | None] = Omitted()
    avatar_url: Omittable[str] = Omitted()
    full_avatar_url: Omittable[str] = Omitted()
    last_access_time: Omittable[datetime] = Omitted()
    is_owner: Omittable[bool] = Omitted()
    is_admin: Omittable[bool] = Omitted()
    join_time: Omittable[datetime] = Omitted()
    permissions: Omittable[Sequence[ChatAdminPermissionType] | None] = Omitted()
