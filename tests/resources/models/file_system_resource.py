"""A file resource in a package."""

from dataclasses import dataclass
from importlib import resources
from importlib.resources.abc import Traversable


@dataclass(slots=True)
class FileResource:
    """Info needed to locate a file or directory in a package.

    The pathname can be to a file or directory.
    """

    anchor: str
    pathname: str

    def traversable(self) -> Traversable:
        """Get a Traversable for the file system pathname."""
        value = resources.files(self.anchor).joinpath(self.pathname)
        return value
