"""Script to generate or regenerate test data."""

from pathlib import Path

import typer

app = typer.Typer()
RESOURCES_PATH = Path(__file__).parent


@app.command()
def stub():
    """This is a stub command."""


if __name__ == "__main__":
    app()
