"""Models used during testing."""

from dataclasses import dataclass
from importlib import resources
from importlib.resources.abc import Traversable


@dataclass
class FileBasedTest:
    """Info needed to locate two files.

    the pathname can be to a file or directory.
    """

    input_anchor: str
    input_pathname: str
    comparison_anchor: str
    comparison_pathname: str

    def input_resource(self) -> Traversable:
        """Get a Traversable representing the input pathname."""
        value = resources.files(self.input_anchor).joinpath(self.input_pathname)
        return value

    def comparison_resource(self) -> Traversable:
        """Get a Traversable representing the comparison pathname."""
        value = resources.files(self.comparison_anchor).joinpath(
            self.comparison_pathname
        )
        return value
