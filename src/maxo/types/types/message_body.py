from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.types.attachments import Attachments
from maxo.types.types.markup_elements import MarkupElements


class MessageBody(MaxoType):
    mid: str
    seq: int
    text: str | None = None
    attachments: list[Attachments] | None = None
    markup: Omittable[list[MarkupElements] | None] = Omitted()
