"""Two file resources in a package.."""

from dataclasses import dataclass

from .file_system_resource import FileResource


@dataclass(slots=True)
class FileComparison:
    """Info needed to locate two filesystem items."""

    input: FileResource
    comparison: FileResource
