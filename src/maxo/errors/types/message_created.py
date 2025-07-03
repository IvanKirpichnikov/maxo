from maxo.errors.base import MaxoError, error


@error
class MessageCreatedLinkIsEmptyError(MaxoError):
    def __str__(self) -> str:
        return "MessageCreated.link is None"


@error
class MessageCreatedBodyIsEmptyError(MaxoError):
    def __str__(self) -> str:
        return "MessageCreated.body is None"


@error
class MessageCreatedStatIsEmptyError(MaxoError):
    def __str__(self) -> str:
        return "MessageCreated.stat is None"
