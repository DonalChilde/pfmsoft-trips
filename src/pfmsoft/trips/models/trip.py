"""Data model for a `Trip`."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from pfmsoft.trips.snippets.datetime.aware_datetime_dataclass import UtcAwareDatetime


@dataclass(slots=True)
class Position:
    """A position, eg. CA or FO."""

    name: str


@dataclass(slots=True)
class TripDatetime:
    """Stores datetime for three locations."""

    utc: UtcAwareDatetime
    lcl_tz_name: str
    hbt_tz_name: str

    def local(self) -> datetime:
        """The local datetime."""
        return self.utc.utc.astimezone(ZoneInfo(self.lcl_tz_name))

    def home_base(self) -> datetime:
        """The home base datetime."""
        return self.utc.utc.astimezone(ZoneInfo(self.hbt_tz_name))


@dataclass(slots=True)
class AirportCode:
    """Airport/city identifiers."""

    iata: str
    icao: str
    tz_name: str


@dataclass(slots=True)
class BaseEquipment:
    """Base and equipment in the bidding context."""

    base: AirportCode
    satellite_base: AirportCode | None
    equipment: str


@dataclass(slots=True)
class Operation:
    """An area of operation."""

    name: str


@dataclass(slots=True)
class Flight:
    """A flight."""

    eq_code: str
    number: str
    departure_station: AirportCode
    depart: TripDatetime
    arrival_station: AirportCode
    arrive: TripDatetime
    deadhead: bool
    deadhead_code: str
    crewmeal: str
    eq_change: bool
    flight_time: timedelta
    operating_time: timedelta
    soft_time: timedelta
    ground_time: timedelta


@dataclass(slots=True)
class Transportation:
    """Transpo."""

    name: str
    phone: str


@dataclass(slots=True)
class Hotel:
    """A Hotel."""

    name: str
    phone: str
    trans: list[Transportation]


@dataclass(slots=True)
class Layover:
    """A Layover."""

    layover_station: AirportCode
    start: TripDatetime
    end: TripDatetime
    hotels: list[Hotel]
    rest: timedelta


@dataclass(slots=True)
class DutyPeriod:
    """A dutyperiod."""

    start_station: AirportCode
    report: TripDatetime
    end_station: AirportCode
    release: TripDatetime
    flights: list[Flight]
    duty: timedelta
    flight_duty: timedelta
    operating_time: timedelta
    flight_time: timedelta
    soft_time: timedelta
    layover: Layover | None


@dataclass(slots=True)
class Trip:
    """A trip."""

    source: str
    trip_number: str
    base_equipment: BaseEquipment
    positions: list[Position]
    operations: list[Operation]
    special_qual: bool
    start_station: AirportCode
    start: TripDatetime
    end_station: AirportCode
    end: TripDatetime
    flight_time: timedelta
    operating_time: timedelta
    soft_time: timedelta
    dutyperiods: list[DutyPeriod]

    def tafb(self) -> timedelta:
        """Calculate TAFB."""
        ...
