from maxo.errors.base import MaxoError, error


@error
class MessageCallbackMessageIsEmptyError(MaxoError):
    def __str__(self) -> str:
        return "MessageCallback.message is None"
