"""Tests for pbs_2022_01."""

import logging
from importlib import resources
from pathlib import Path

import pytest
from pbs_parse.pbs_2022_01.models.structured import STRUCTURED_TRIP_SERIALIZER

from pfmsoft.trips.models.trip import serialize_trip
from pfmsoft.trips.translate import pbs_2022_01 as pbs
from tests.resources.models import FileBasedTest
from tests.resources.structured_trips import STRUCTURED_TRIPS_ANCHOR
from tests.resources.trips import TRIPS_ANCHOR

logger = logging.getLogger(__name__)

OUTPUT_PATH = f"trips/structured/{Path(__file__).stem}"

items = [
    FileBasedTest(
        input_anchor=STRUCTURED_TRIPS_ANCHOR,
        input_pathname="PBS_BOS_November_2024_20241010125404.page_102_of_103.trip_2_of_4.parsed.structured.json",
        comparison_anchor=TRIPS_ANCHOR,
        comparison_pathname="",
    ),
    FileBasedTest(
        input_anchor=STRUCTURED_TRIPS_ANCHOR,
        input_pathname="PBS_PHX_November_2024_20241010130419.page_7_of_261.trip_3_of_5.parsed.structured.json",
        comparison_anchor=TRIPS_ANCHOR,
        comparison_pathname="",
    ),
]
PARSE_ONLY = False


def idfn(val: FileBasedTest) -> str:
    """Return a custom test name for parameterized tests."""
    return "data"


@pytest.mark.parametrize("with_loaded_file", items)
def test_with_loaded_file(test_output_dir: Path, with_loaded_file: FileBasedTest):
    """Translate with pre-loaded file."""
    with resources.as_file(with_loaded_file.input_resource()) as input_path:
        s_trip = STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=input_path)
        trips = pbs.translate_structured_trip(s_trip=s_trip)
    path_out_dir = test_output_dir / OUTPUT_PATH / "test_with_loaded_file"
    for trip in trips:
        path_out = path_out_dir / trip.default_file_name(trip)
        serialize_trip(path_out=path_out, trip=trip)
    expected_count = int(s_trip.ops_count)
    output_count = len(list(path_out_dir.glob(f"*_{trips[0].trip_number}.*")))
    assert expected_count == output_count


@pytest.mark.parametrize("with_loaded_file", items)
def test_with_file_path(test_output_dir: Path, with_loaded_file: FileBasedTest):
    """Translate with file path."""
    with resources.as_file(with_loaded_file.input_resource()) as input_path:
        # load the trip anyway for comparison info
        s_trip = STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=input_path)
        trips = pbs.translate_structured_trip_from_file(path_in=input_path)
    path_out_dir = test_output_dir / OUTPUT_PATH / "test_with_file_path"
    for trip in trips:
        path_out = path_out_dir / trip.default_file_name(trip)
        serialize_trip(path_out=path_out, trip=trip)
    expected_count = int(s_trip.ops_count)
    output_count = len(list(path_out_dir.glob(f"*_{trips[0].trip_number}.*")))
    assert expected_count == output_count
