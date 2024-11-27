"""Pydantic model of a trip."""

from datetime import timedelta

from pydantic import AwareDatetime, BaseModel

from .utc_datetime_validator import UtcDatetime


class Position(BaseModel):
    """A position, eg. CA or FO."""

    name: str


class DatetimeTriple(BaseModel):
    """Stores datetime for three locations."""

    utc: UtcDatetime
    lcl: AwareDatetime
    hbt: AwareDatetime


class AirportCode(BaseModel):
    """Airport/city identifiers."""

    iata: str
    icao: str
    tz_name: str


class BaseEquipment(BaseModel):
    """Base and equipment in the bidding context."""

    base: AirportCode
    satellite_base: AirportCode
    equipment: str


class Operation(BaseModel):
    """An area of operation."""

    name: str


class Flight(BaseModel):
    """A flight."""

    eq_code: str
    number: str
    departure_station: AirportCode
    depart: DatetimeTriple
    arrival_station: AirportCode
    arrive: DatetimeTriple
    deadhead: bool
    crewmeal: str
    eq_change: bool
    ground_time: timedelta

    def block_time(self) -> timedelta:
        """Calculate the block time from arrive and depart."""
        ...


class Transportation(BaseModel):
    """Transpo."""

    name: str
    phone: str


class Hotel(BaseModel):
    """A Hotel."""

    name: str
    phone: str
    trans: list[Transportation]


class Layover(BaseModel):
    """A Layover."""

    layover_station: AirportCode
    start: DatetimeTriple
    end: DatetimeTriple
    hotels: list[Hotel]

    def rest(self) -> timedelta:
        """Calculate rest time."""
        ...


class DutyPeriod(BaseModel):
    """A dutyperiod."""

    start_station: AirportCode
    start: DatetimeTriple
    end_station: AirportCode
    end: DatetimeTriple
    flights: list[Flight]
    flight_duty: timedelta
    layover: Layover | None

    def duty_time(self) -> timedelta:
        """Calculate duty time."""
        ...


class Trip(BaseModel):
    """A trip."""

    trip_number: str
    base: BaseEquipment
    positions: list[Position]
    operations: list[Operation]
    special_qual: bool
    start_station: AirportCode
    start: DatetimeTriple
    end_station: AirportCode
    end: DatetimeTriple
    soft_time: timedelta
    dutyperiods: list[DutyPeriod]

    def tafb(self) -> timedelta:
        """Calculate TAFB."""
        ...
