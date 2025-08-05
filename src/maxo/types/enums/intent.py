from enum import StrEnum


class IntentType(StrEnum):
    """
    Намерение кнопки.

    Влияет на отображение клиентом.

    Attributes:
        default:
        positive:
        negative:

    """

    DEFAULT = "default"
    POSITIVE = "positive"
    NEGATIVE = "negative"
