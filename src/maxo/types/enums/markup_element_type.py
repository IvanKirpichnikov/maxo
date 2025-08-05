from enum import StrEnum


class MarkupElementType(StrEnum):
    STRONG = "strong"
    EMPHASIZED = "emphasized"
    MONOSPACED = "monospaced"
    LINK = "link"
    STRIKETHROUGH = "strikethrough"
    UNDERLINE = "underline"
    USER_MENTION = "user_mention"
    HEADING = "heading"
    HIGHLIGHTED = "highlighted"
