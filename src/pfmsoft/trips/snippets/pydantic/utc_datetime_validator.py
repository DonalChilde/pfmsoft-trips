"""Pydantic validator for utc datetime."""

from typing import Annotated

from pydantic import AwareDatetime
from pydantic.functional_validators import AfterValidator

from ..datetime.check_utc import UTC_NAMES, check_tz_name_for_utc


def check_utc(v: AwareDatetime) -> AwareDatetime:
    """Ensure value is an aware datetime that is UTC."""
    if not check_tz_name_for_utc(v):
        raise ValueError(
            f"Value might be a non-utc datetime. tzname={v.tzname()} "
            f"is not on approved list {UTC_NAMES!r} {v!r}"
        )

    return v


UtcDatetime = Annotated[AwareDatetime, AfterValidator(check_utc)]
