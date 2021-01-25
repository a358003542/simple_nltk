# Natural Language Toolkit: Corpus Readers
#
# Copyright (C) 2001-2020 simple_nltk Project
# Author: Edward Loper <edloper@gmail.com>
# URL: <http://simple_nltk.org/>
# For license information, see LICENSE.TXT

# TODO this docstring isn't up-to-date!
"""
simple_nltk corpus readers.  The modules in this package provide functions
that can be used to read corpus files in a variety of formats.  These
functions can be used to read both the corpus files that are
distributed in the simple_nltk corpus package, and corpus files that are part
of external corpora.

Available Corpora
=================

Please see http://www.simple_nltk.org/simple_nltk_data/ for a complete list.
Install corpora using simple_nltk.download().

Corpus Reader Functions
=======================
Each corpus module defines one or more "corpus reader functions",
which can be used to read documents from that corpus.  These functions
take an argument, ``item``, which is used to indicate which document
should be read from the corpus:

- If ``item`` is one of the unique identifiers listed in the corpus
  module's ``items`` variable, then the corresponding document will
  be loaded from the simple_nltk corpus package.
- If ``item`` is a filename, then that file will be read.

Additionally, corpus reader functions can be given lists of item
names; in which case, they will return a concatenation of the
corresponding documents.

Corpus reader functions are named based on the type of information
they return.  Some common examples, and their return types, are:

- words(): list of str
- sents(): list of (list of str)
- paras(): list of (list of (list of str))
- tagged_words(): list of (str,str) tuple
- tagged_sents(): list of (list of (str,str))
- tagged_paras(): list of (list of (list of (str,str)))
- chunked_sents(): list of (Tree w/ (str,str) leaves)
- parsed_sents(): list of (Tree with str leaves)
- parsed_paras(): list of (list of (Tree with str leaves))
- xml(): A single xml ElementTree
- raw(): unprocessed corpus contents

For example, to read a list of the words in the Brown Corpus, use
``simple_nltk.corpus.brown.words()``:

"""

import re

from simple_nltk.tokenize import RegexpTokenizer
from simple_nltk.corpus.util import LazyCorpusLoader
from simple_nltk.corpus.reader import *

stopwords = LazyCorpusLoader(
    "stopwords", WordListCorpusReader, r"(?!README|\.).*", encoding="utf8"
)
