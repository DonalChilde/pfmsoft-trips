"""Translate a pbs_2022_01 format trip."""

import logging
from collections.abc import Sequence
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pbs_parse.pbs_2022_01.models.structured as ST

from pfmsoft.trips.models import trip as model

logger = logging.getLogger(__name__)


def translate_structured_trip_from_file(path_in: Path) -> list[model.Trip]:
    """Load a pbs_2022_01 structured trip from file and translate it to Trip."""
    s_trip = ST.structured_trip_serializer().load_from_json(path_in=path_in)
    return translate_structured_trip(s_trip=s_trip)


def translate_structured_trip(s_trip: ST.StructuredTrip) -> list[model.Trip]:
    """Translate a pbs_2022_01 structured trip to Trip."""
    return _translate_trips(s_trip=s_trip)


def _translate_flight(
    departure_utc: datetime, base: model.AirportCode, s_flight: ST.Flight
) -> model.Flight:
    departure_station = get_airport_code_from_iata(iata=s_flight.departure_station)
    depart = build_datetime_triple(
        utc_date=departure_utc, base=base, local=departure_station
    )
    arrival_station = get_airport_code_from_iata(iata=s_flight.arrival_station)
    try:
        operating_time = ST.parse_duration(s_flight.block)
    except ValueError as e:
        logger.info(
            f"Error parsing block duration {s_flight.block}. Is this a deadhead? {e}"
        )
        operating_time = timedelta(hours=0)
    arrive = calculate_arrival(
        departure_station=departure_station,
        arrival_station=arrival_station,
        departure=depart,
        arrival_time=s_flight.arrival_time,
    )
    flight_time = arrive.utc - depart.utc
    soft_time = ST.parse_duration(s_flight.synth)
    try:
        ground_time = ST.parse_duration(s_flight.ground)
    except ValueError:
        ground_time = timedelta(hours=0)

    return model.Flight(
        eq_code=s_flight.eq_code,
        number=s_flight.flight_number,
        departure_station=departure_station,
        depart=depart,
        arrival_station=arrival_station,
        arrive=arrive,
        deadhead=bool(s_flight.deadhead),
        deadhead_code=s_flight.deadhead_code,
        crewmeal=s_flight.crew_meal,
        eq_change=bool(s_flight.equipment_change),
        flight_time=flight_time,
        operating_time=operating_time,
        soft_time=soft_time,
        ground_time=ground_time,
    )


def _translate_flights(
    dutyperiod_report: datetime, base: model.AirportCode, s_flights: Sequence[ST.Flight]
) -> list[model.Flight]:
    flights: list[model.Flight] = []
    departure_utc = (
        dutyperiod_report  # FIXME this needs to be offset to real departure time
    )
    for s_flight in s_flights:
        flight = _translate_flight(
            departure_utc=departure_utc, base=base, s_flight=s_flight
        )
        departure_utc = flight.arrive.utc + flight.ground_time
        flights.append(flight)
    return flights


def _translate_dutyperiod(
    report_utc: datetime, base: model.AirportCode, s_dutyperiod: ST.DutyPeriod
) -> model.DutyPeriod:
    start_station = get_airport_code_from_iata(
        iata=s_dutyperiod.flights[0].departure_station
    )
    end_station = get_airport_code_from_iata(s_dutyperiod.flights[-1].arrival_station)
    report = build_datetime_triple(utc_date=report_utc, base=base, local=start_station)
    duty = ST.parse_duration(s_dutyperiod.duty)
    release_utc = report.utc + duty
    release = build_datetime_triple(utc_date=release_utc, base=base, local=end_station)
    flight_duty = ST.parse_duration(s_dutyperiod.flight_duty)
    operating_time = ST.parse_duration(s_dutyperiod.block)
    soft_time = ST.parse_duration(s_dutyperiod.synth)
    flights = _translate_flights(
        dutyperiod_report=report.utc, base=base, s_flights=s_dutyperiod.flights
    )
    layover = _translate_layover(
        dutyperiod_release=release.utc, base=base, s_layover=s_dutyperiod.layover
    )
    flight_time = timedelta(seconds=sum([x.flight_time.seconds for x in flights]))
    return model.DutyPeriod(
        start_station=start_station,
        report=report,
        end_station=end_station,
        release=release,
        flights=flights,
        duty=duty,
        flight_duty=flight_duty,
        flight_time=flight_time,
        operating_time=operating_time,
        soft_time=soft_time,
        layover=layover,
    )


def _translate_dutyperiods(
    first_report: datetime,
    base: model.AirportCode,
    s_dutyperiods: Sequence[ST.DutyPeriod],
) -> list[model.DutyPeriod]:
    dutyperiods: list[model.DutyPeriod] = []
    report_utc = first_report
    for s_dutyperiod in s_dutyperiods:
        dutyperiod = _translate_dutyperiod(
            report_utc=report_utc, base=base, s_dutyperiod=s_dutyperiod
        )
        dutyperiods.append(dutyperiod)
        if dutyperiod.layover is not None:
            report_utc = dutyperiod.release.utc + dutyperiod.layover.rest
    return dutyperiods


def _translate_layover(
    dutyperiod_release: datetime, base: model.AirportCode, s_layover: ST.Layover | None
) -> model.Layover | None:
    if s_layover is None:
        return None
    hotels = _translate_hotels(s_hotels=s_layover.hotels)
    layover_station = get_airport_code_from_iata(iata=s_layover.city)
    start = build_datetime_triple(
        utc_date=dutyperiod_release, base=base, local=layover_station
    )
    rest = ST.parse_duration(s_layover.rest)
    end_utc = dutyperiod_release + rest
    end = build_datetime_triple(utc_date=end_utc, base=base, local=layover_station)
    return model.Layover(
        layover_station=layover_station, start=start, end=end, rest=rest, hotels=hotels
    )


def _translate_hotel(s_hotel: ST.Hotel) -> model.Hotel:
    transportation: list[model.Transportation] = []
    for s_trans in s_hotel.transportation:
        trans = model.Transportation(name=s_trans.name, phone=s_trans.phone)
        transportation.append(trans)
    hotel = model.Hotel(name=s_hotel.name, phone=s_hotel.phone, trans=transportation)
    return hotel


def _translate_hotels(s_hotels: Sequence[ST.Hotel]) -> list[model.Hotel]:
    hotels: list[model.Hotel] = []
    for s_hotel in s_hotels:
        hotels.append(_translate_hotel(s_hotel=s_hotel))
    return hotels


def _transate_trip(s_trip: ST.StructuredTrip, start_date: date) -> model.Trip:
    """Translate a StructuredTrip that starts on a particular date."""
    base_airport = get_airport_code_from_iata(s_trip.page_footer.base)

    first_report = s_trip.dutyperiods[0].report_time
    trip_start = trip_start_utc(
        start_date=start_date, first_report=first_report, tz_name=base_airport.tz_name
    )
    dutyperiods = _translate_dutyperiods(
        first_report=trip_start,
        base=base_airport,
        s_dutyperiods=s_trip.dutyperiods,
    )
    positions = [model.Position(name=x) for x in s_trip.positions]
    operations = [model.Operation(name=x) for x in s_trip.operations]
    flight_time = timedelta(seconds=sum([x.flight_time.seconds for x in dutyperiods]))
    operating_time = ST.parse_duration(s_trip.block)
    soft_time = ST.parse_duration(s_trip.synth)
    try:
        satellite_base = get_airport_code_from_iata(
            iata=s_trip.page_footer.satellite_base
        )
    except ValueError:
        satellite_base = None
    base_equipment = model.BaseEquipment(
        base=base_airport,
        satellite_base=satellite_base,
        equipment=s_trip.page_footer.equipment,
    )
    return model.Trip(
        source=s_trip.uuid,
        trip_number=s_trip.number,
        base_equipment=base_equipment,
        positions=positions,
        operations=operations,
        special_qual=bool(s_trip.qualifications),
        start_station=dutyperiods[0].start_station,
        start=dutyperiods[0].report,
        end_station=dutyperiods[-1].end_station,
        end=dutyperiods[-1].release,
        flight_time=flight_time,
        operating_time=operating_time,
        soft_time=soft_time,
        dutyperiods=dutyperiods,
    )


def _translate_trips(s_trip: ST.StructuredTrip) -> list[model.Trip]:
    start_dates = ST.build_start_dates(
        effective_from=date.fromisoformat(s_trip.external.effective_from),
        effective_to=date.fromisoformat(s_trip.external.effective_to),
        calendar=s_trip.calendar,
    )
    trips: list[model.Trip] = []
    for start_date in start_dates:
        trip = _transate_trip(s_trip=s_trip, start_date=start_date)
        trips.append(trip)
    return trips


def get_airport_code_from_iata(iata: str) -> model.AirportCode:
    """Get airport info from database."""
    # raise ValueError if not found.
    pass


def trip_start_utc(start_date: date, first_report: str, tz_name: str) -> datetime:
    """summary.

    _extended_summary_

    Args:
        start_date (_type_): _description_
        first_report (_type_): _description_
        tz_name (_type_): _description_

    Returns:
        _type_: _description_
    """
    pass


def build_datetime_triple(
    utc_date: datetime, base: model.AirportCode, local: model.AirportCode
) -> model.DatetimeTriple:
    """Build a DatetimeTriple."""
    return model.DatetimeTriple(
        utc=utc_date,
        lcl=utc_date.astimezone(ZoneInfo(local.tz_name)),
        hbt=utc_date.astimezone(ZoneInfo(base.tz_name)),
    )


def calculate_arrival(
    departure_station: model.AirportCode,
    departure: model.DatetimeTriple,
    arrival_station: model.AirportCode,
    arrival_time: str,
) -> model.DatetimeTriple:
    """Derive the utc arrival time, and use to build DatetimeTriple."""
