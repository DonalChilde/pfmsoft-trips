"""Tests for pbs_2022_01."""

import logging
from importlib import resources
from pathlib import Path

import pytest
from pbs_parse.pbs_2022_01.models.structured import STRUCTURED_TRIP_SERIALIZER

from pfmsoft.trips.models.pydantic.trip import serialize_trip
from pfmsoft.trips.translate import pbs_2022_01 as pbs
from tests.resources.models.file_comparison import FileComparison
from tests.resources.models.file_system_resource import FileResource
from tests.resources.pbs_2022_01.structured_trips import STRUCTURED_TRIPS_ANCHOR

logger = logging.getLogger(__name__)

OUTPUT_PATH = f"trips/translate_and_compare/pbs_2022_01/{Path(__file__).stem}"

items = [
    FileComparison(
        input=FileResource(anchor=STRUCTURED_TRIPS_ANCHOR, pathname=""),
        comparison=FileResource(anchor="", pathname=""),
    ),
]


def idfn(val: FileResource) -> str:
    """Return a custom test name for parameterized tests."""
    return "Translate_and_compare_"


def test_translate_and_compare(test_output_dir: Path):
    """Translate and compare with expected results."""
    pass


# @pytest.mark.parametrize("with_loaded_file", items)
# def test_with_loaded_file(test_output_dir: Path, with_loaded_file: FileResource):
#     """Translate with pre-loaded file."""
#     with resources.as_file(with_loaded_file.traversable()) as input_path:
#         s_trip = STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=input_path)
#         trips = pbs.translate_structured_trip(s_trip=s_trip)
#     path_out_dir = test_output_dir / OUTPUT_PATH / "test_with_loaded_file"
#     for trip in trips:
#         path_out = path_out_dir / trip.default_file_name(trip)
#         serialize_trip(path_out=path_out, trip=trip)
#     expected_count = int(s_trip.ops_count)
#     output_count = len(list(path_out_dir.glob(f"*_{trips[0].trip_number}.*")))
#     assert expected_count == output_count


# @pytest.mark.parametrize("with_loaded_file", items)
# def test_with_file_path(test_output_dir: Path, with_loaded_file: FileResource):
#     """Translate with file path."""
#     with resources.as_file(with_loaded_file.traversable()) as input_path:
#         # load the trip anyway for comparison info
#         s_trip = STRUCTURED_TRIP_SERIALIZER.load_from_json(path_in=input_path)
#         trips = pbs.translate_structured_trip_from_file(path_in=input_path)
#     path_out_dir = test_output_dir / OUTPUT_PATH / "test_with_file_path"
#     for trip in trips:
#         path_out = path_out_dir / trip.default_file_name(trip)
#         serialize_trip(path_out=path_out, trip=trip)
#     expected_count = int(s_trip.ops_count)
#     output_count = len(list(path_out_dir.glob(f"*_{trips[0].trip_number}.*")))
#     assert expected_count == output_count
