# -*- coding: utf-8 -*-

'''
 BAF documentation build configuration file, created by
 sphinx-quickstart on Mon Jan 27 12:50:29 2014.
'''

# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# The names of the variables in this file are Sphinx keywords so
# we can't make them uppercase as pylint demands.
# pylint: disable=invalid-name

import os
import sys
import subprocess
import enum

docs_dir = os.path.dirname(os.path.abspath(__file__))

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
sys.path.insert(0, os.path.join(docs_dir, "_ext"))

# A simple function interface_example.py is included in this directory to
# show proper sphinx documentation of code. In order to find this file,
# the current directory must be added to Python's system path:
sys.path.insert(0, os.path.abspath('../infrastructure/build/fab'))

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# We need version >=  1.8 for the html_css_files feature.
needs_sphinx = '1.8'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'autoapi.sphinx',
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.githubpages',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
]

#autoapi_modules = {'baf': {'output': '_autogenerated/autoapi'}}
#autoapi_ignore = ["*/test_*.py"]

# Enable numbered referencing of figures (use with :numref:`my-fig-reference`)
numfig = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'BAF'
project_copyright = '2024-2025 Bureau of Meteorology'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#

version = "0.1-dev"
release = "0.1.0-dev"
# pylint: enable=undefined-variable

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = 'pydata_sphinx_theme'
html_theme = "sphinx_rtd_theme"

# Create a link to the doxygen documentation that can be used from the rst files
base_url = os.getenv('READTHEDOCS_CANONICAL_URL', '/')
rst_epilog = f"""
.. _Doxygen Documentation: {base_url}html
"""

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = ['theme_overrides.css']  # override wide tables in RTD theme

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'bafdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author,
#  documentclass [howto/manual]).
latex_documents = [
    ('index', 'baf.tex', 'BAF User Guide',
     'Joerg Henrichs, Junwei Lyu', 'manual'),
]

# Set maximum depth for the nested lists to prevent LaTeX
# "too deeply nested" build failures when using whitespaces instead
# of tabs in documentation (there must be an indentation of at least
# three spaces when nesting a list within another). This is a known
# Docutils failure, see e.g. here:
# https://docutils.sourceforge.io/docs/dev/todo.html
# LaTeX can have up to 6 lists (of any sort) nested, 4 "enumerate"
# environments among the set of nested lists and 4 "itemize"
# environments among the set of nested lists, see e.g. here
# https://texfaq.org/FAQ-toodeep
latex_elements = {
    'maxlistdepth': '6',
}

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'baf', 'BAF Documentation',
     ['Joerg Henrichs, Junwei Lyu'], 1)
]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ('index', 'baf', 'BAF Documentation',
     'Joerg Henrichs, Lunwei Lyu',
     'baf',
     'Build Architecture with Fab.',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = 'BAF User Guide'
epub_author = 'Joerg Henrichs, Junwei Lyu'
epub_publisher = 'Joerg Henrichs, Junwei Lyu'
epub_copyright = project_copyright

# The language of the text. It defaults to the language option
# or en if the language is not set.
# epub_language = ''

# The scheme of the identifier. Typical schemes are ISBN or URL.
# epub_scheme = ''

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
# epub_identifier = ''

# A unique identification for the text.
# epub_uid = ''

# A tuple containing the cover image and cover page html template filenames.
# epub_cover = ()

# HTML files that should be inserted before the pages created by sphinx.
# The format is a list of tuples containing the path and title.
# epub_pre_files = []

# HTML files shat should be inserted after the pages created by sphinx.
# The format is a list of tuples containing the path and title.
# epub_post_files = []

# A list of files that should not be packed into the epub file.
# epub_exclude_files = []

# The depth of the table of contents in toc.ncx.
# epub_tocdepth = 3

# Allow duplicate toc entries.
# epub_tocdup = True


# -- Options for linkcheck -------------------------------------------------

linkcheck_anchors = True
# We need to ignore this anchor (used a couple of times in examples.rst)
# because it seems that GitHub's JavaScript-generated page defeats the
# link checker.
linkcheck_anchors_ignore = ['user-content-netcdf-library-lfric-examples']

linkcheck_ignore = [
    # Auto-generated (used for doxygen and apilinks)
    r'^../_autogenerated',
    r'^/html',
    # Sphinx has problems with Github anchors, so we skip
    # the links to anchors to the main README.
    r'^https://github.com/MetOffice/lfric-baf#',
]

# -- Autodoc configuration ---------------------------------------------------


# def remove_op_enum_attrib_docstring(app, what, name, obj, skip, options):
#     '''
#     A handler that ensures any EnumType objects named 'Operator' are *not*
#     documented. This is required to avoid warnings of the form:

#         psyclone/psyir/nodes/operation.py:docstring of
#         psyclone.psyir.nodes.operation.Operator:1: WARNING: duplicate object
#         description of psyclone.psyir.nodes.operation.Operator, other instance
#         in autogenerated/psyclone.psyir.nodes, use :no-index: for one of them

#     '''
#     # EnumMeta is used for compatibility with Python < 3.11.
#     if name.endswith("Operator") and isinstance(obj, enum.EnumMeta):
#         return True
#     return skip


def setup(app):
    '''
    Add in our custom handler to avoid documentation warnings for the various
    Operator members of psyir.nodes.*Operation.

    '''
    # app.connect('autodoc-skip-member', remove_op_enum_attrib_docstring)
    pass


# -- Generate the Doxygen documentation --------------------------------------
#subprocess.call(
#    'cd reference_guide; '
#    'mkdir -p ../_autogenerated/doxygen; '
#    'doxygen doxygen.config',
#    shell=True)
# Include doxygen-generated documentation into Sphinx output
#html_extra_path = ['_autogenerated/doxygen']
