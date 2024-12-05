"""Pydantic validator for utc datetime."""

from datetime import UTC
from typing import Annotated

from pydantic import AwareDatetime
from pydantic.functional_validators import AfterValidator


def check_utc(v: AwareDatetime) -> AwareDatetime:
    """Ensure value is an aware datetime that is UTC."""
    assert v.tzinfo == UTC, f"Value is a non-utc datetime. {v!r}"
    return v


UtcDatetime = Annotated[AwareDatetime, AfterValidator(check_utc)]
