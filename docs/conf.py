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
sys.path.insert(0, os.path.abspath('../src/so_magic'))

# Please use the Sphinx format for writting docstrings (other fornats include Google and Numpy which require the 'napoleon' extension). 

# -- Project information -----------------------------------------------------

project = 'so-magic'
copyright = '2020, Konstantinos Lampridis'
author = 'Konstantinos Lampridis'

# The full version, including alpha/beta/rc tags
release = '0.7.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinxcontrib.spelling'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

# on_rtd is whether we are on readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only set the theme if we're building docs locally
    html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']


### External Links Configuration ###
# provided by the sphinx.ext.extlinks extension

# With the current settings (see the mapping below), you can for example use the directive :issue:`50`, which will
# render a link with text 'issue 50' which upon clicking redirects to https://github.com/peterwittek/somoclu/issues/50

# Mapping of link identifiers/keys to:
# 2-length tuples with 1st item the url and 2nd the prefix (the "text string")
extlinks = {
    'issue': (
        'https://github.com/peterwittek/somoclu/issues/%s',
        'issue '
    ),
}
