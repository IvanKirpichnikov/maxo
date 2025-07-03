from maxo.errors.base import MaxoError, error


@error
class EmptyStateError(MaxoError):
    pass
