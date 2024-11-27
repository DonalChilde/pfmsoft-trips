"""Define a model for an instant in time."""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from pydantic import AwareDatetime, BaseModel, ConfigDict


class Instant(BaseModel):
    """Represents an instant in time.

    The datetime should be an aware datetime with a timezone of timezone.utc
    The tz_name field can store the local time zone name for conversions.
    Addition and subtraction of timedeltas is supported.
    Enforced use of utc time should prevent ambiguous math.
    """

    model_config = ConfigDict(frozen=True)

    utc_date: AwareDatetime
    tz_name: str

    def localize(self) -> datetime:
        """Get the localized datetime."""
        return self.utc_date.astimezone(tz=ZoneInfo(self.tz_name))

    def replace(
        self, utc_date: datetime | None = None, tz_name: str | None = None
    ) -> "Instant":
        """Replace some values and return a new Instant."""
        if utc_date is None and tz_name is None:
            raise ValueError("Must supply a value to replace to get new Instant.")
        if utc_date is not None and tz_name is not None:
            return Instant(utc_date=utc_date, tz_name=tz_name)
        if utc_date is not None:
            return Instant(utc_date=utc_date, tz_name=self.tz_name)
        assert tz_name is not None
        return Instant(utc_date=self.utc_date, tz_name=tz_name)

    def __copy__(self) -> "Instant":
        """Return a copy of this Instant."""
        return Instant(utc_date=self.utc_date, tz_name=self.tz_name)

    def __add__(self, other: timedelta) -> "Instant":
        """Add a timedelta, and return a new Instant with the same tz_name."""
        if not isinstance(other, timedelta):  # type: ignore
            return NotImplemented
        new_instant = Instant(utc_date=self.utc_date + other, tz_name=self.tz_name)
        return new_instant

    def __sub__(self, other: timedelta) -> "Instant":
        """Subtract a timedelta, and return a new Instant with the same tz_name."""
        if not isinstance(other, timedelta):  # type: ignore
            return NotImplemented
        new_instant = Instant(utc_date=self.utc_date - other, tz_name=self.tz_name)
        return new_instant

    def __str__(self) -> str:
        """Get string representation."""
        return (
            f"utc_date={self.utc_date.isoformat()}, tz_name={self.tz_name}, "
            f"local={self.localize().isoformat()}"
        )

    def __repr__(self) -> str:
        """Get repr."""
        return (
            f"{self.__class__.__qualname__}("
            f"utc_date={self.utc_date!r}, tz_name={self.tz_name!r}"
            ")"
        )

    # def __eq__(self, __value: object) -> bool:
    #     if isinstance(__value, Instant):
    #         return (self.utc_date, self.tz_name) == (__value.utc_date, __value.tz_name)
    #     return NotImplemented
