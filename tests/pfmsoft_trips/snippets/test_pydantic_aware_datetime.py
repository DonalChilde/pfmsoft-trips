"""Tests for AwareDatetime validation with pydantic."""

import logging
from datetime import UTC, datetime
from zoneinfo import ZoneInfo  # , available_timezones

import pytest
from pydantic_core import ValidationError

from pfmsoft.trips.snippets.pydantic.aware_datetime_pydantic import AwareDatetime

logger = logging.getLogger(__name__)


def test_non_utc_datetime():
    """Test for bad inputs."""
    # Nieve datetime
    with pytest.raises(ValidationError) as exc_info:
        nieve_dt = datetime.now()
        _ = AwareDatetime(utc=nieve_dt, tz_name="America/New_York")
    logger.info(exc_info)

    # non utc datetime
    with pytest.raises(ValidationError) as exc_info:
        tzinfo = ZoneInfo("America/New_York")
        non_utc_dt = datetime.now(tz=tzinfo)
        _ = AwareDatetime(utc=non_utc_dt, tz_name="America/New_York")
    logger.info(exc_info)

    # Bad tz_name
    with pytest.raises(ValidationError) as exc_info:
        tzinfo = ZoneInfo("UTC")
        non_utc_dt = datetime.now(tz=tzinfo)
        _ = AwareDatetime(utc=non_utc_dt, tz_name="foo")
    logger.info(exc_info)

    tzinfo = ZoneInfo("UTC")
    utc_dt = datetime.now(tz=tzinfo)
    _ = AwareDatetime(utc=utc_dt, tz_name="America/New_York")


def test_utc():
    utc = datetime.now(tz=UTC)
    aware = AwareDatetime(utc=utc, tz_name="UTC")
    logger.info(aware)
    logger.info(repr(aware))
    logger.info(repr(AwareDatetime(utc=aware.localize(), tz_name="UTC")))
    assert aware.tzinfo.utcoffset(None) == UTC.utcoffset(None)
    assert aware.utc == aware.localize()


# def test_log_tz_names():
#     logger.info(available_timezones())
#     utc_names = ["UTC", "Zulu", "Etc/UTC"]
#     foo = datetime.now(UTC)
#     assert foo.tzname() in utc_names
