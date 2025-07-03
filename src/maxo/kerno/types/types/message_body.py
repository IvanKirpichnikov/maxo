from maxo.kerno.types.base import MaxoType
from maxo.kerno.types.types.attachments import Attachments
from maxo.kerno.types.types.markup_elements import MarkupElements
from maxo.omit import Omittable, Omitted


class MessageBody(MaxoType):
    mid: str
    seq: int
    text: str | None = None
    attachments: list[Attachments] | None = None
    markup: Omittable[list[MarkupElements] | None] = Omitted()
