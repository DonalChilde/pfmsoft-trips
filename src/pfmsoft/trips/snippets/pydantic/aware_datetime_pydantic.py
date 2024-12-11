"""Define a model for an AwareDatetime pydantic dataclass."""

import dataclasses
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic.dataclasses import dataclass
from pydantic_extra_types.timezone_name import TimeZoneName

from .utc_datetime_validator import UtcDatetime


@dataclass(slots=True, frozen=True)
class AwareDatetime:
    """Represents a local time zone aware UTC datetime.

    AwareDatetime is used as a replacement for an non-utc aware datetime.

    Math on non-utc aware datetimes can have unexpected results due to DST,
    Where math with utc aware datetimes delivers consistent results.

    Using AwareDatetime, the datetime is always kept in utc until needed in the
    local timezone.

    Args:
        utc (UtcDatetime): An aware datetime with a timezone of 'UTC'.
        tz_name (TimeZoneName): The str name of the localized timezone.

    Raises:
        ValueError: For an error in creating tzinfo from tz_name.

    """

    utc: UtcDatetime
    tz_name: TimeZoneName
    localized: datetime = dataclasses.field(init=False)  # type: ignore

    def __post_init__(self):
        """Assign the localized field."""
        try:
            tzinfo = ZoneInfo(self.tz_name)
        except ZoneInfoNotFoundError as err:
            raise ValueError(
                f"Tried to create an AwareDatetime with an invalid tz_name. {self!r}"
            ) from err
        object.__setattr__(self, "localized", self.utc.astimezone(tzinfo))

    @property
    def localized(self) -> datetime:
        """The localized datetime."""
        return self.localized

    def replace(
        self, utc: datetime | None = None, tz_name: TimeZoneName | None = None
    ) -> "AwareDatetime":
        """Replace some values and return a new AwareDatetime."""
        if utc is None:
            utc = self.utc
        if tz_name is None:
            tz_name = self.tz_name
        return AwareDatetime(utc=utc, tz_name=tz_name)

    def __copy__(self) -> "AwareDatetime":
        """Return a copy of this Instant."""
        return AwareDatetime(utc=self.utc, tz_name=self.tz_name)

    def __add__(self, other: timedelta) -> "AwareDatetime":
        """Add a timedelta, and return a new AwareDatetime with the same tz_name."""
        if not isinstance(other, timedelta):  # type: ignore
            return NotImplemented
        new_instant = AwareDatetime(utc=self.utc + other, tz_name=self.tz_name)
        return new_instant

    def __sub__(self, other: "timedelta|AwareDatetime") -> "timedelta|AwareDatetime":
        """Subtract a timedelta or an AwareDatetime.

        Subtracting a timedelta returns a new AwareDatetime with the same tz_name.
        Subtracting an AwareDatetime returns a timedelta.
        This mirrors the behavior of datetime.
        """
        if not isinstance(other, timedelta | AwareDatetime):  # type: ignore
            return NotImplemented
        if isinstance(other, timedelta):
            return AwareDatetime(utc=self.utc - other, tz_name=self.tz_name)
        return self.utc - other.utc

    def __str__(self) -> str:
        """Get string representation."""
        return f"AwareDatetime({self.localized.isoformat()}[{self.tz_name}])"

    def __repr__(self) -> str:
        """Get repr."""
        return (
            f"{self.__class__.__qualname__}("
            f"utc={self.utc!r}, tz_name={self.tz_name!r}"
            ")"
        )
