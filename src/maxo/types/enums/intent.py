from enum import Enum


class IntentType(str, Enum):
    DEFAULT = "default"
    POSITIVE = "positive"
    NEGATIVE = "negative"
