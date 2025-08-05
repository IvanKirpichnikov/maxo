from dataclasses import dataclass
from random import normalvariate


@dataclass(slots=True, frozen=True)
class BackoffConfig:
    min_delay: float
    max_delay: float
    factor: float
    jitter: float

    def __post_init__(self) -> None:
        if self.max_delay <= self.min_delay:
            raise ValueError("`max_delay` should be greater than `min_delay`")
        if self.factor <= 1:
            raise ValueError("`factor` should be greater than 1")


class Backoff:
    def __init__(
        self,
        config: BackoffConfig,
    ) -> None:
        self._config = config
        self._current_delay = 0.0
        self._next_delay = config.min_delay
        self._counter = 0

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(tryings={self._counter}, "
            f"current_delay={self._current_delay}, "
            f"next_delay={self._next_delay})"
        )

    @property
    def counter(self) -> int:
        return self.counter

    @property
    def current_delay(self) -> float:
        return self._current_delay

    def calc_next_delay(self, current_delay: float) -> float:
        config = self._config
        mean = min(current_delay * config.factor, config.max_delay)
        return normalvariate(mean, config.jitter)

    def next(self) -> None:
        self._counter += 1
        self._current_delay = self._next_delay
        self._next_delay = self.calc_next_delay(self._current_delay)

    def reset(self) -> None:
        self._counter = 0
        self._current_delay = 0.0
        self._next_delay = self._config.min_delay
