# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import sys
import papis
import docutils

from docutils.parsers.rst import Directive
from sphinx_click.ext import ClickDirective

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.inheritance_diagram",
    "sphinx_click.ext",
]

intersphinx_mapping = {
    "bibtexparser": ("https://bibtexparser.readthedocs.io/en/main", None),
    "click": ("https://click.palletsprojects.com/en/latest", None),
    "python": ("https://docs.python.org/3", None),
    "requests": ("https://requests.readthedocs.io/en/latest", None),
    "stevedore": ("https://docs.openstack.org/stevedore/latest", None),
}

autodoc_member_order = "bysource"


# Exec directive {{{

class CustomClickDirective(ClickDirective):
    def run(self):
        sections = super().run()

        # NOTE: just remove the title section so we can add our own
        return sections[0].children[1:]


class PapisConfig(Directive):
    has_content = True
    optional_arguments = 3
    required_arguments = 1
    option_spec = {"default": str, "section": str, "description": str}
    add_index = True

    def run(self):
        from papis.config import get_general_settings_name, get_default_settings
        key = self.arguments[0]
        section = self.options.get(
            "section",
            get_general_settings_name())
        default = self.options.get(
            "default",
            get_default_settings().get(section, {}).get(key, "<missing>"))

        lines = []
        lines.append("")
        lines.append(".. _config-{section}-{key}:".format(section=section, key=key))
        lines.append("")
        lines.append("`{key} <config-{section}-{key}>`_"
                     .format(section=section, key=key))

        if "\n" in str(default):
            lines.append("    - **Default**: ")
            lines.append("        .. code::")
            lines.append("")
            for lindef in default.split("\n"):
                lines.append(3 * "    " + lindef)
        else:
            lines.append("    - **Default**: ``{value!r}``"
                         .format(value=default))
        lines.append("")

        view = docutils.statemachine.ViewList(lines)
        self.content = view + self.content

        node = docutils.nodes.paragraph()
        node.document = self.state.document
        self.state.nested_parse(self.content, self.content_offset, node)

        return node.children


def setup(app):
    app.add_directive("click", CustomClickDirective, override=True)
    app.add_directive("papis-config", PapisConfig)


# }}} Exec directive #

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "papis"
copyright = "2017, Alejandro Gallo"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = papis.__version__
# The full version, including alpha/beta/rc tags.
# release = re.sub('^v', '', os.popen('git describe').read().strip())
release = version

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
exclude_patterns = [
    "commands/*.rst",
    "default-settings.rst",
]

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
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

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
htmlhelp_basename = "papisdoc"

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ("index", "papis.tex", "papis Documentation", "Alejandro Gallo", "manual"),
]

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

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ("index", "papis", "Papis Documentation",
     ["Alejandro Gallo"], 1),
    ("configuration", "papis-config", "Papis Configuration",
     ["Alejandro Gallo"], 1),
    ("commands/add", "papis-add", "add command",
     ["Alejandro Gallo"], 1),
    ("commands/addto", "papis-addto", "addto command",
     ["Alejandro Gallo"], 1),
    ("commands/browse", "papis-browse", "browse command",
     ["Alejandro Gallo"], 1),
    ("commands/config", "papis-config", "config command",
     ["Alejandro Gallo"], 1),
    ("commands/default", "papis-default", "default command",
     ["Alejandro Gallo"], 1),
    ("commands/edit", "papis-edit", "edit command",
     ["Alejandro Gallo"], 1),
    ("commands/explore", "papis-explore", "explore command",
     ["Alejandro Gallo"], 1),
    ("commands/export", "papis-export", "export command",
     ["Alejandro Gallo"], 1),
    ("commands/git", "papis-git", "git command",
     ["Alejandro Gallo"], 1),
    ("commands/list", "papis-list", "list command",
     ["Alejandro Gallo"], 1),
    ("commands/mv", "papis-mv", "mv command",
     ["Alejandro Gallo"], 1),
    ("commands/open", "papis-open", "open command",
     ["Alejandro Gallo"], 1),
    ("commands/rename", "papis-rename", "rename command",
     ["Alejandro Gallo"], 1),
    ("commands/rm", "papis-rm", "rm command",
     ["Alejandro Gallo"], 1),
    ("commands/run", "papis-run", "run command",
     ["Alejandro Gallo"], 1),
    ("commands/update", "papis-update", "update command",
     ["Alejandro Gallo"], 1),
]

# If true, show URL addresses after external links.
# man_show_urls = False

# -- Options for Texinfo output {{{1 ------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    ("index", "papis", "papis Documentation",
     "Alejandro Gallo", "papis", "One line description of project.",
     "Miscellaneous"),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False

# -- Options for Epub output {{{1 --------------------------------------------

# Bibliographic Dublin Core info.
epub_title = "papis"
epub_author = "Alejandro Gallo"
epub_publisher = "Alejandro Gallo"
epub_copyright = "2017, Alejandro Gallo"
# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]
