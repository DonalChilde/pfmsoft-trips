"""Pydantic validator for utc datetime."""

from datetime import timedelta
from typing import Annotated

from pydantic import AwareDatetime
from pydantic.functional_validators import AfterValidator

utc_names = ["UTC", "Zulu", "Etc/UTC"]


def check_utc(v: AwareDatetime) -> AwareDatetime:
    """Ensure value is an aware datetime that is UTC.

    This is a bit of a hack. May show true for some non-UTC times.
    Possibly test for tz_name as one of the various utc names?
    """
    assert v.tzinfo is not None
    assert v.utcoffset() == timedelta(), f"Value is a non-utc datetime. {v!r}"
    assert (
        v.tzname() in utc_names
    ), f"Value is a non-utc datetime. tzname={v.tzname()} is not on approved list {utc_names!r} {v!r}"
    return v


UtcDatetime = Annotated[AwareDatetime, AfterValidator(check_utc)]
