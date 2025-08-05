from maxo.errors.base import MaxoError, maxo_error


@maxo_error
class StateError(MaxoError):
    message: str

    def __str__(self) -> str:
        return self.message
