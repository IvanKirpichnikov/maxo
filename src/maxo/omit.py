from typing import TypeAlias, TypeVar

# TODO: придумать, как избавиться от этого костыля.
from retejo.core.markers import (
    Omitted as OriginOmitted,
    is_defined as origin_is_defined,
    is_not_defined as origin_is_not_defined,
    is_not_omittable_tp as origin_is_not_omittable_tp,
    is_not_omitted as origin_is_not_omitted,
    is_omittable_tp as origin_is_omittable_tp,
    is_omitted as origin_is_omitted,
)

T = TypeVar("T")

Omittable: TypeAlias = T | OriginOmitted
Omitted = OriginOmitted
is_defined = origin_is_defined
is_not_defined = origin_is_not_defined
is_not_omittable_tp = origin_is_not_omittable_tp
is_not_omitted = origin_is_not_omitted
is_omittable_tp = origin_is_omittable_tp
is_omitted = origin_is_omitted

__all__ = [
    "Omittable",
    "Omitted",
    "is_defined",
    "is_not_defined",
    "is_not_omittable_tp",
    "is_not_omitted",
    "is_omittable_tp",
    "is_omitted",
]
