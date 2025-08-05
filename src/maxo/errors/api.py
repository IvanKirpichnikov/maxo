from maxo.errors.base import MaxoError, maxo_error


@maxo_error
class MaxBotApiError(MaxoError):
    code: str
    message: str


@maxo_error
class MaxBotBadRequestError(MaxBotApiError): ...


@maxo_error
class MaxVotForbiddenError(MaxBotApiError): ...


@maxo_error
class MaxBotUnauthorizedError(MaxBotApiError): ...


@maxo_error
class MaxBotNotFoundError(MaxBotApiError): ...


@maxo_error
class MaxBotMethodNotAllowedError(MaxBotApiError): ...


@maxo_error
class MaxBotTooManyRequestsError(MaxBotApiError): ...


@maxo_error
class MaxBotServiceUnavailableError(MaxBotApiError): ...


@maxo_error
class RetvalReturnedServerException(MaxoError): ...  # noqa: N818
