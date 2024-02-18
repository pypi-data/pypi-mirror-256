# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

import simulai

# -- Project information -----------------------------------------------------

project = "simulai"
copyright = "2023, IBM"
author = "IBM"
version = "latest"

# -- General configuration

extensions = [
    # "numpydoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
]

napoleon_use_param = True
napoleon_use_ivar = True

autodoc_mock_imports = ["mpi4py", "numpy", "simulai", "sphinx-press-theme"]
suppress_warnings = ["autosectionlabel.*"]


# Napoleon settings
# napoleon_numpy_docstring = True

# html_context configuration for GitHub edit link
html_context = {
    "display_github": True,
    "github_user": "promptslab",
    "github_repo": "Promptify",
    "github_version": "main",
    "conf_py_path": "docs/",
}


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "TODO/*",
]

source_suffix = [".rst", ".md"]

# -- Options for HTML output -------------------------------------------------

# -- Options for HTML output
html_theme = "press"


# Below html_theme_options config depends on the theme.
html_logo = "../assets/logo.png"

gettext_additional_targets = ["literal-block", "image"]

html_theme_options = {
    "logo_only": True,
    "display_version": True,
    "sidebarbgcolor": "#FFF8DC",
    "sidebartextcolor": "#000000",
    "sidebarlinkcolor": "#444444",
    "relbartextcolor": "#000000",
    "collapsiblesidebar": True,
    "body_max_width": "90%",
    "sidebarwidth": "30%",
    "globaltoc_maxdepth": 10,
}


autodoc_typehints_format = "short"
python_use_unqualified_type_names = True

# -- Options for EPUB output
epub_show_urls = "footnote"
