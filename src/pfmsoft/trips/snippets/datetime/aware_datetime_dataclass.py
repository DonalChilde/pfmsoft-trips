"""Define a model for an AwareDatetime dataclass."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from functools import cached_property
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


@dataclass(frozen=True, slots=True)
class AwareDatetime:
    """Represents a time zone aware UTC datetime.

    The datetime should be an aware datetime with a timezone of timezone.utc
    The tz_name field stores the local time zone name.
    Addition and subtraction of timedeltas is supported.
    Enforced use of utc time should prevent ambiguous math.
    """

    utc: datetime
    tz_name: str = "UTC"

    def __post_init__(self):
        """Make sure that the values are valid."""
        if self.utc.tzinfo is None:
            raise ValueError(
                f"Tried to create an AwareDatetime using a datetime with no tzinfo. datetime tzinfo must be UTC. {self!r}"
            )
        if self.utc.tzinfo != UTC:
            raise ValueError(
                f"Tried to create an AwareDatetime with a non-utc datetime. datetime tzinfo must be UTC. {self!r}"
            )
        # Make sure the tz_name is valid by getting the tzinfo.
        _ = self.tzinfo

    @cached_property
    def tzinfo(self) -> ZoneInfo:
        """Get the tzinfo."""
        try:
            return ZoneInfo(self.tz_name)
        except ZoneInfoNotFoundError as err:
            raise ValueError(
                f"Tried to create an AwareDatetime with an invalid tz_name. {self!r}"
            ) from err

    def localize(self) -> datetime:
        """Get the localized datetime."""
        return self.utc.astimezone(tz=self.tzinfo)

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
        return f"AwareDatetime({self.localize().isoformat()}[{self.tz_name}])"

    def __repr__(self) -> str:
        """Get repr."""
        return (
            f"{self.__class__.__qualname__}("
            f"utc={self.utc!r}, tz_name={self.tz_name!r}"
            ")"
        )

    # def __eq__(self, __value: object) -> bool:
    #     """Test for equality."""
    #     if isinstance(__value, Instant):
    #         return (self.utc_date, self.tz_name) == (__value.utc_date, __value.tz_name)
    #     return NotImplemented


# class Instant(BaseModel):
#     """Represents an instant in time.

#     The datetime should be an aware datetime with a timezone of timezone.utc
#     The tz_name field can store the local time zone name for conversions.
#     Addition and subtraction of timedeltas is supported.
#     Enforced use of utc time should prevent ambiguous math.
#     """

#     model_config = ConfigDict(frozen=True)

#     utc_date: datetime
#     tz_name: str

#     def localize(self, tz_name: str | None = None) -> datetime:
#         if tz_name is None:
#             return self.utc_date.astimezone(tz=ZoneInfo(self.tz_name))
#         return self.utc_date.astimezone(tz=ZoneInfo(tz_name))

#     def replace(
#         self, utc_date: datetime | None = None, tz_name: str | None = None
#     ) -> "Instant":
#         if utc_date is None and tz_name is None:
#             raise ValueError("Must supply a value to replace to get new Instant.")
#         if utc_date is not None and tz_name is not None:
#             return Instant(utc_date=utc_date, tz_name=tz_name)
#         if utc_date is not None:
#             return Instant(utc_date=utc_date, tz_name=self.tz_name)
#         assert tz_name is not None
#         return Instant(utc_date=self.utc_date, tz_name=tz_name)

#     def __copy__(self) -> "Instant":
#         return Instant(utc_date=self.utc_date, tz_name=self.tz_name)

#     def __add__(self, other: timedelta) -> "Instant":
#         if not isinstance(other, timedelta):
#             return NotImplemented
#         new_instant = Instant(utc_date=self.utc_date + other, tz_name=self.tz_name)
#         return new_instant

#     def __sub__(self, other: timedelta) -> "Instant":
#         if not isinstance(other, timedelta):
#             return NotImplemented
#         new_instant = Instant(utc_date=self.utc_date - other, tz_name=self.tz_name)
#         return new_instant

#     def __str__(self) -> str:
#         return (
#             f"utc_date={self.utc_date.isoformat()}, tz_name={self.tz_name}, "
#             f"local={self.localize().isoformat()}"
#         )

#     def __repr__(self) -> str:
#         return (
#             f"{self.__class__.__qualname__}("
#             f"utc_date={self.utc_date!r}, tz_name={self.tz_name!r}"
#             ")"
#         )

#     def __eq__(self, __value: object) -> bool:
#         if isinstance(__value, Instant):
#             return (self.utc_date, self.tz_name) == (__value.utc_date, __value.tz_name)
#         return NotImplemented
