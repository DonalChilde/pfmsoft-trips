"""Pydantic model of a trip."""

from datetime import timedelta

from pydantic import AwareDatetime, BaseModel, computed_field

from .utc_datetime_validator import UtcDatetime


class Position(BaseModel):
    """A position, eg. CA or FO."""

    name: str


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
    depart: UtcDatetime
    arrival_station: AirportCode
    arrive: UtcDatetime
    deadhead: bool
    crewmeal: str
    eq_change: bool
    ground_time: timedelta

    def block_time(self) -> timedelta:
        """Calculate the block time from arrive and depart."""
        ...

    def depart_lcl(self) -> AwareDatetime:
        """Departure time as local time."""
        ...

    def arrive_lcl(self) -> AwareDatetime:
        """Arrival time as local time."""
        ...

    def depart_hbt(self) -> AwareDatetime:
        """Departure time as home base time."""
        ...

    def arrive_hbt(self) -> AwareDatetime:
        """Arrival time as home base time."""
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
    start: UtcDatetime
    end: UtcDatetime
    hotels: list[Hotel]

    def rest(self) -> timedelta:
        """Calculate rest time."""
        ...

    def start_lcl(self) -> AwareDatetime:
        """Layover start as local time."""
        ...

    def end_lcl(self) -> AwareDatetime:
        """Layover end as local time."""
        ...

    def start_hbt(self) -> AwareDatetime:
        """Layover start as home base time."""
        ...

    def end_hbt(self) -> AwareDatetime:
        """Layover end as home base time."""
        ...


class DutyPeriod(BaseModel):
    """A dutyperiod."""

    start_station: AirportCode
    start: UtcDatetime
    end_station: AirportCode
    end: UtcDatetime
    flights: list[Flight]
    flight_duty: timedelta
    layover: Layover | None

    def duty_time(self) -> timedelta:
        """Calculate duty time."""
        ...

    def start_lcl(self) -> AwareDatetime:
        """Dutyperiod start as local time."""
        ...

    def end_lcl(self) -> AwareDatetime:
        """Dutyperiod end as local time."""
        ...

    def start_hbt(self) -> AwareDatetime:
        """Dutyperiod start as home base time."""
        ...

    def end_hbt(self) -> AwareDatetime:
        """Dutyperiod end as home base time."""
        ...


class Trip(BaseModel):
    """A trip."""

    trip_number: str
    base: BaseEquipment
    positions: list[Position]
    operations: list[Operation]
    special_qual: bool
    start_station: AirportCode
    start: UtcDatetime
    end_station: AirportCode
    end: UtcDatetime
    soft_time: timedelta
    dutyperiods: list[DutyPeriod]

    def tafb(self) -> timedelta:
        """Calculate TAFB."""
        ...

    @computed_field
    @property
    def start_lcl(self) -> AwareDatetime:
        """Trip start as local time."""
        ...

    @computed_field
    @property
    def end_lcl(self) -> AwareDatetime:
        """Trip end as local time."""
        ...

    @computed_field
    @property
    def start_hbt(self) -> AwareDatetime:
        """Trip start as home base time."""
        ...

    @computed_field
    @property
    def end_hbt(self) -> AwareDatetime:
        """Trip end as home base time."""
        ...
