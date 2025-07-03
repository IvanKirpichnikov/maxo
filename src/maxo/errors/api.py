from maxo.errors.base import MaxoError, error


@error
class MaxBotApiError(MaxoError):
    code: str
    message: str


@error
class MaxBotBadRequestError(MaxBotApiError): ...


@error
class MaxVotForbiddenError(MaxBotApiError): ...


@error
class MaxBotUnauthorizedError(MaxBotApiError): ...


@error
class MaxBotNotFoundError(MaxBotApiError): ...


@error
class MaxBotMethodNotAllowedError(MaxBotApiError): ...


@error
class MaxBotTooManyRequestsError(MaxBotApiError): ...


@error
class MaxBotServiceUnavailableError(MaxBotApiError): ...
