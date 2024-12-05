"""Cli for translating to Trips."""

import logging
from pathlib import Path
from typing import Annotated

import typer

logger = logging.getLogger(__name__)

app = typer.Typer()


@app.command()
def trip(
    ctx: typer.Context,
    path_in: Annotated[
        Path,
        typer.Argument(
            help="source IndexedStrings.json file.", exists=True, file_okay=True
        ),
    ],
    path_out: Annotated[
        Path, typer.Argument(help="destination directory for parsed trip.")
    ],
    file_name: Annotated[
        Path | None,
        typer.Option(help="file name for output if differrent from default."),
    ] = None,
    overwrite: Annotated[
        bool, typer.Option(help="Overwrite existing output file.")
    ] = False,
    input_format: Annotated[str, typer.Argument(help="The input format.")] = "",
):
    """Translate one file here."""


@app.command()
def all():
    """Translate all the files here."""


@app.command()
def available_inputs():
    """List the possible inputs here."""


if __name__ == "__main__":
    app()
