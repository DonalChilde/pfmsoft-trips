"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

# loading project metadata from the pyproject.toml file
# requires python >=3.11
import tomllib

with open("../../pyproject.toml", "rb") as f:
    toml_data = tomllib.load(f)

# make sure that the src dir is on the path to support autodoc, version, etc
sys.path.insert(0, os.path.abspath("../../src"))
from pfmsoft_trips import (  # pylint: disable=wrong-import-position
    __release__,
    __version__,
)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = toml_data["project"]["name"]
author = ",".join([author["name"] for author in toml_data["project"]["authors"]])
project_copyright = f"2024, {author}"
# The full version, including alpha/beta/rc tags.
release = __release__
# The short X.Y.Z version.
version = __version__


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinxcontrib.typer",
]
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# exclude_patterns = []

# Mapping Example
# intersphinx_mapping = {
#     "python": ("https://docs.python.org/3", None),
#     "aiohttp_queue": ("https://pfmsoft-aiohttp-queue.readthedocs.io/en/latest/", None),
# }
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

# The suffix(es) of source filenames.
# You can specify multiple suffixes as a dict:
#
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "restructuredtext",
    ".md": "markdown",
}

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
