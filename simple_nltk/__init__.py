# Natural Language Toolkit (simple_nltk)
#
# Copyright (C) 2001-2020 simple_nltk Project
# Authors: Steven Bird <stevenbird1@gmail.com>
#          Edward Loper <edloper@gmail.com>
# URL: <http://simple_nltk.org/>
# For license information, see LICENSE.TXT

"""
The Natural Language Toolkit (simple_nltk) is an open source Python library
for Natural Language Processing.  A free online book is available.
(If you use the library for academic research, please cite the book.)

Steven Bird, Ewan Klein, and Edward Loper (2009).
Natural Language Processing with Python.  O'Reilly Media Inc.
http://simple_nltk.org/book
"""

import os

# //////////////////////////////////////////////////////
# Metadata
# //////////////////////////////////////////////////////

# Version.  For each new release, the version number should be updated
# in the file VERSION.
try:
    # If a VERSION file exists, use it!
    version_file = os.path.join(os.path.dirname(__file__), "../VERSION")
    with open(version_file, "r") as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = "unknown (running code interactively?)"
except IOError as ex:
    __version__ = "unknown (%s)" % ex

if __doc__ is not None:  # fix for the ``python -OO``
    __doc__ += "\n@version: " + __version__


# Copyright notice
__copyright__ = """\
Copyright (C) 2001-2020 simple_nltk Project.

Distributed and Licensed under the Apache License, Version 2.0,
which is included by reference.
"""

__license__ = "Apache License, Version 2.0"
# Description of the toolkit, keywords, and the project's primary URL.
__longdescr__ = """\
The Natural Language Toolkit (simple_nltk) is a Python package for
natural language processing.  simple_nltk requires Python 2.6 or higher."""
__keywords__ = [
    "NLP",
    "CL",
    "natural language processing",
    "computational linguistics",
    "parsing",
    "tagging",
    "tokenizing",
    "syntax",
    "linguistics",
    "language",
    "natural language",
    "text analytics",
]
__url__ = "http://simple_nltk.org/"

# Maintainer, contributors, etc.
__maintainer__ = "Steven Bird, Edward Loper, Ewan Klein"
__maintainer_email__ = "stevenbird1@gmail.com"
__author__ = __maintainer__
__author_email__ = __maintainer_email__

from simple_nltk.internals import config_java

# support numpy from pypy
try:
    import numpypy
except ImportError:
    pass

# Override missing methods on environments where it cannot be used like GAE.
import subprocess

if not hasattr(subprocess, "PIPE"):

    def _fake_PIPE(*args, **kwargs):
        raise NotImplementedError("subprocess.PIPE is not supported.")

    subprocess.PIPE = _fake_PIPE
if not hasattr(subprocess, "Popen"):

    def _fake_Popen(*args, **kwargs):
        raise NotImplementedError("subprocess.Popen is not supported.")

    subprocess.Popen = _fake_Popen

###########################################################
# TOP-LEVEL MODULES
###########################################################

# Import top-level functionality into top-level namespace

from simple_nltk.collocations import *
from simple_nltk.decorators import decorator, memoize
from simple_nltk.featstruct import *
from simple_nltk.grammar import *
from simple_nltk.probability import *
from simple_nltk.text import *
from simple_nltk.tree import *
from simple_nltk.util import *
from simple_nltk.jsontags import *

###########################################################
# PACKAGES
###########################################################

from simple_nltk.chunk import *
from simple_nltk.classify import *
from simple_nltk.inference import *
from simple_nltk.metrics import *
from simple_nltk.parse import *
from simple_nltk.tag import *
from simple_nltk.tokenize import *
from simple_nltk.sem import *
from simple_nltk.stem import *

# explicitly import all top-level modules (ensuring
# they override the same names inadvertently imported
# from a subpackage)

from simple_nltk import ccg, chunk, classify, collocations
from simple_nltk import data, featstruct, grammar, help, inference, metrics
from simple_nltk import misc, parse, probability, sem, stem
from simple_nltk import tag, tbl, text, tokenize, tree, treetransforms, util


# FIXME:  override any accidentally imported demo, see https://github.com/simple_nltk/simple_nltk/issues/2116
def demo():
    print("To run the demo code for a module, type simple_nltk.module.demo()")
