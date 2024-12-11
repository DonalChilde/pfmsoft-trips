"""Tests for AwareDatetime."""

import logging
from datetime import UTC, datetime
from zoneinfo import ZoneInfo

import pytest

from pfmsoft.trips.snippets.datetime.aware_datetime_dataclass import (
    AwareDatetime,
    UtcAwareDatetime,
)

logger = logging.getLogger(__name__)


def test_utc_aware_datetime_construction():
    """Test the construction of UtcAwareDatetime."""
    # normal creation
    dt_utc = datetime.now(UTC)
    aware = UtcAwareDatetime(utc=dt_utc)
    assert aware.utc == aware.localized
    assert aware.tz_name == "UTC"
    logger.info("%r, localized: %s", aware, aware.localized.isoformat())

    dt_utc = datetime.now(ZoneInfo("UTC"))
    aware = UtcAwareDatetime(utc=dt_utc)
    assert aware.utc == aware.localized
    assert aware.tz_name == "UTC"
    logger.info("%r, localized: %s", aware, aware.localized.isoformat())

    dt_utc = datetime.now(ZoneInfo("Etc/UTC"))
    aware = UtcAwareDatetime(utc=dt_utc)
    assert aware.utc == aware.localized
    assert aware.tz_name == "UTC"
    logger.info("%r, localized: %s", aware, aware.localized.isoformat())

    dt_utc = datetime.now(ZoneInfo("Zulu"))
    aware = UtcAwareDatetime(utc=dt_utc)
    assert aware.utc == aware.localized
    assert aware.tz_name == "UTC"
    logger.info("%r, localized: %s", aware, aware.localized.isoformat())

    # nieve datetime
    dt_nieve = datetime.now()
    with pytest.raises(ValueError) as err:
        aware = UtcAwareDatetime(utc=dt_nieve)
    logger.info(err)

    # aware datetime, not utc
    dt_aware = datetime.now(ZoneInfo("America/Phoenix"))
    with pytest.raises(ValueError) as err:
        aware = UtcAwareDatetime(utc=dt_aware)
    logger.exception(err)


def test_aware_datetime_construction():
    """Test the construction of AwareDatetime."""
    # normal creation
    dt_utc = datetime.now(UTC)
    aware = AwareDatetime(utc=dt_utc, tz_name="America/Phoenix")
    logger.info("%r, localized: %s", aware, aware.localized.isoformat())

    dt_utc = datetime.now(ZoneInfo("UTC"))
    aware = AwareDatetime(utc=dt_utc, tz_name="America/Phoenix")
    logger.info("%r, localized: %s", aware, aware.localized.isoformat())

    dt_utc = datetime.now(ZoneInfo("Etc/UTC"))
    aware = AwareDatetime(utc=dt_utc, tz_name="America/Phoenix")
    logger.info("%r, localized: %s", aware, aware.localized.isoformat())

    dt_utc = datetime.now(ZoneInfo("Zulu"))
    aware = AwareDatetime(utc=dt_utc, tz_name="America/Phoenix")
    logger.info("%r, localized: %s", aware, aware.localized.isoformat())

    # nieve datetime
    dt_nieve = datetime.now()
    with pytest.raises(ValueError):
        aware = AwareDatetime(utc=dt_nieve, tz_name="America/Phoenix")

    # aware datetime, not utc
    dt_aware = datetime.now(ZoneInfo("America/Phoenix"))
    with pytest.raises(ValueError):
        aware = AwareDatetime(utc=dt_aware, tz_name="America/Phoenix")

    # Bad tz_name
    dt_utc = datetime.now(UTC)
    with pytest.raises(ValueError):
        aware = AwareDatetime(utc=dt_utc, tz_name="Foo")
