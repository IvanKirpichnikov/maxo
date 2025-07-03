from enum import Enum


class MarkupElementType(str, Enum):
    STRONG = "strong"
    EMPHASIZED = "emphasized"
    MONOSPACED = "monospaced"
    LINK = "link"
    STRIKETHROUGH = "strikethrough"
    UNDERLINE = "underline"
    USER_MENTION = "user_mention"
    HEADING = "heading"
    HIGHLIGHTED = "highlighted"
