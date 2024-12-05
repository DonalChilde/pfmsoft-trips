"""Pydantic model of a trip."""

from datetime import timedelta
from pathlib import Path

from pydantic import AwareDatetime, BaseModel

from pfmsoft.trips.airports import airport_from_iata
from pfmsoft.trips.snippets.file.check_file import check_file

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
    satellite_base: AirportCode | None
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
    deadhead_code: str
    crewmeal: str
    eq_change: bool
    flight_time: timedelta
    operating_time: timedelta
    soft_time: timedelta
    ground_time: timedelta


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
    rest: timedelta


class DutyPeriod(BaseModel):
    """A dutyperiod."""

    start_station: AirportCode
    report: DatetimeTriple
    end_station: AirportCode
    release: DatetimeTriple
    flights: list[Flight]
    duty: timedelta
    flight_duty: timedelta
    operating_time: timedelta
    flight_time: timedelta
    soft_time: timedelta
    layover: Layover | None


class Trip(BaseModel):
    """A trip."""

    source: str
    trip_number: str
    base_equipment: BaseEquipment
    positions: list[Position]
    operations: list[Operation]
    special_qual: bool
    start_station: AirportCode
    start: DatetimeTriple
    end_station: AirportCode
    end: DatetimeTriple
    flight_time: timedelta
    operating_time: timedelta
    soft_time: timedelta
    dutyperiods: list[DutyPeriod]

    def tafb(self) -> timedelta:
        """Calculate TAFB."""
        ...

    @staticmethod
    def default_file_name(trip: "Trip") -> str:
        """The default file name for a Trip."""
        if trip.base_equipment.satellite_base is None:
            base_fragment = (
                f"{trip.base_equipment.base.iata}_{trip.base_equipment.equipment}"
            )
        else:
            base_fragment = f"{trip.base_equipment.base.iata}_{trip.base_equipment.satellite_base.iata}_{trip.base_equipment.equipment}"

        file_name = f"{trip.start.lcl.date().isoformat()}_{base_fragment}_{trip.trip_number}.json"
        return file_name


def get_airport_code_from_iata(iata: str) -> AirportCode:
    """Get airport info from database."""
    airport = airport_from_iata(iata=iata)
    return AirportCode(
        iata=airport["iata"], icao=airport["icao"], tz_name=airport["tz"]
    )


def serialize_trip(path_out: Path, trip: Trip):
    """Save a trip to json."""
    check_file(path_out=path_out)
    path_out.write_text(trip.model_dump_json(indent=1))
