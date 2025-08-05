from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class EmphasizedMarkupElement(MaxoType):
    from_: int
    length: int


class HeadingMarkupElement(MaxoType):
    from_: int
    length: int


class HighlightedMarkupElement(MaxoType):
    from_: int
    length: int


class LinkMarkupElement(MaxoType):
    from_: int
    length: int
    url: Omittable[str] = Omitted()


class MonospacedMarkupElements(MaxoType):
    from_: int
    length: int


class StrikethroughMarkupElement(MaxoType):
    from_: int
    length: int


class StrongMarkupElement(MaxoType):
    from_: int
    length: int


class UnderlineMarkupElement(MaxoType):
    from_: int
    length: int


class UserMentionMarkupElement(MaxoType):
    from_: int
    length: int
    user_link: Omittable[str | None] = Omitted()
    user_id: Omittable[int | None] = Omitted()


MarkupElements = (
    EmphasizedMarkupElement
    | HeadingMarkupElement
    | HighlightedMarkupElement
    | LinkMarkupElement
    | UserMentionMarkupElement
    | UnderlineMarkupElement
    | MonospacedMarkupElements
    | StrongMarkupElement
    | StrikethroughMarkupElement
)
