"""Define a model for an AwareDatetime dataclass."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .check_utc import check_tz_name_for_utc


@dataclass(frozen=True, kw_only=True, slots=True)
class AwareDatetime:
    """Represents a local time zone aware UTC datetime.

    AwareDatetime is used as a replacement for an non-utc aware datetime.

    Math on non-utc aware datetimes can have unexpected results due to DST,
    Where math with utc aware datetimes delivers consistent results.

    Using AwareDatetime, the datetime is always kept in utc until needed in the
    local timezone.

    Args:
        utc (datetime): An aware datetime with a timezone of 'UTC'.
        tz_name (str): The name of the localized timezone.

    Raises:
        ValueError: For an error in creating tzinfo from tz_name, or for using
            a non UTC datetime for utc.

    """

    utc: datetime
    tz_name: str
    localized: datetime = field(init=False)  # type: ignore

    def __post_init__(self):
        """Make sure that the values are valid."""
        try:
            tzinfo = ZoneInfo(self.tz_name)
        except ZoneInfoNotFoundError as err:
            raise ValueError(
                f"Tried to create an AwareDatetime with an invalid tz_name. {self!r}"
            ) from err
        object.__setattr__(self, "localized", self.utc.astimezone(tzinfo))

        if self.utc.tzinfo is None:
            raise ValueError(
                f"Tried to create an AwareDatetime using a datetime with no tzinfo. datetime tzinfo must be `UTC`. {self!r}"
            )
        if not check_tz_name_for_utc(self.utc):
            raise ValueError(
                f"Tried to create an AwareDatetime with a non-utc datetime. datetime tzinfo must be `UTC`. {self!r}"
            )

    @property
    def localized(self) -> datetime:
        """The localized datetime."""
        return self.localized

    def replace(
        self, utc: datetime | None = None, tz_name: str | None = None
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


@dataclass(frozen=True, slots=True)
class UtcAwareDatetime(AwareDatetime):
    """Represents a time zone aware UTC datetime.

    UtcAwareDatetime is used as a replacement for an non-utc aware datetime.


    Math on non-utc aware datetimes can have unexpected results due to DST,
    Where math with utc aware datetimes delivers consistent results.

    Using UtcAwareDatetime, the datetime is always kept in utc.

    Args:
        utc (datetime): An aware datetime with a timezone of 'UTC'.
        tz_name (str): The name of the utc timezone.

    Raises:
        ValueError: For using a non UTC datetime for utc.

    """

    tz_name: str = field(init=False)

    def __post_init__(self):
        """Make sure that the values are valid.

        tz_name will be the same as reported by self.utc.tz_name().
        localized will be self.utc
        """
        # These have to go first, else the raised exceptions will
        # throw an AttributeError.
        object.__setattr__(self, "tz_name", self.utc.tzname())
        object.__setattr__(self, "localized", self.utc)
        if self.utc.tzinfo is None:
            raise ValueError(
                f"Tried to create an AwareDatetime using a datetime with no tzinfo. datetime tzinfo must be `UTC`. {self!r}"
            )
        if not check_tz_name_for_utc(self.utc):
            raise ValueError(
                f"Tried to create an AwareDatetime with a non-utc datetime. datetime tzinfo must be `UTC`. {self!r}"
            )
