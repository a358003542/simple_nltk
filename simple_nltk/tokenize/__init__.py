# -*- coding: utf-8 -*-
# Natural Language Toolkit: Tokenizers
#
# Copyright (C) 2001-2020 simple_nltk Project
# Author: Edward Loper <edloper@gmail.com>
#         Steven Bird <stevenbird1@gmail.com> (minor additions)
# Contributors: matthewmc, clouds56
# URL: <http://simple_nltk.org/>
# For license information, see LICENSE.TXT

r"""
simple_nltk Tokenizer Package

Tokenizers divide strings into lists of substrings.  For example,
tokenizers can be used to find the words and punctuation in a string:

    >>> from simple_nltk.tokenize import word_tokenize
    >>> s = '''Good muffins cost $3.88\nin New York.  Please buy me
    ... two of them.\n\nThanks.'''
    >>> word_tokenize(s)
    ['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York', '.',
    'Please', 'buy', 'me', 'two', 'of', 'them', '.', 'Thanks', '.']

This particular tokenizer requires the Punkt sentence tokenization
models to be installed. simple_nltk also provides a simpler,
regular-expression based tokenizer, which splits text on whitespace
and punctuation:

    >>> from simple_nltk.tokenize import wordpunct_tokenize
    >>> wordpunct_tokenize(s)
    ['Good', 'muffins', 'cost', '$', '3', '.', '88', 'in', 'New', 'York', '.',
    'Please', 'buy', 'me', 'two', 'of', 'them', '.', 'Thanks', '.']

We can also operate at the level of sentences, using the sentence
tokenizer directly as follows:

    >>> from simple_nltk.tokenize import simple_sent_tokenize, word_tokenize
    >>> simple_sent_tokenize(s)
    ['Good muffins cost $3.88\nin New York.', 'Please buy me\ntwo of them.', 'Thanks.']
    >>> [word_tokenize(t) for t in simple_sent_tokenize(s)]
    [['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York', '.'],
    ['Please', 'buy', 'me', 'two', 'of', 'them', '.'], ['Thanks', '.']]

Caution: when tokenizing a Unicode string, make sure you are not
using an encoded version of the string (it may be necessary to
decode it first, e.g. with ``s.decode("utf8")``.

simple_nltk tokenizers can produce token-spans, represented as tuples of integers
having the same semantics as string slices, to support efficient comparison
of tokenizers.  (These methods are implemented as generators.)

    >>> from simple_nltk.tokenize import WhitespaceTokenizer
    >>> list(WhitespaceTokenizer().span_tokenize(s))
    [(0, 4), (5, 12), (13, 17), (18, 23), (24, 26), (27, 30), (31, 36), (38, 44),
    (45, 48), (49, 51), (52, 55), (56, 58), (59, 64), (66, 73)]

There are numerous ways to tokenize text.  If you need more control over
tokenization, see the other methods provided in this package.

For further information, please see Chapter 3 of the simple_nltk book.
"""

import re

from simple_nltk.data import load
from simple_nltk.tokenize.mwe import MWETokenizer
from simple_nltk.tokenize.destructive import simple_nltkWordTokenizer
from simple_nltk.tokenize.punkt import PunktSentenceTokenizer
from simple_nltk.tokenize.regexp import (
    RegexpTokenizer,
    WhitespaceTokenizer,
    BlanklineTokenizer,
    WordPunctTokenizer,
    wordpunct_tokenize,
    regexp_tokenize,
    blankline_tokenize,
)
from simple_nltk.tokenize.repp import ReppTokenizer
from simple_nltk.tokenize.sexpr import SExprTokenizer, sexpr_tokenize
from simple_nltk.tokenize.simple import (
    SpaceTokenizer,
    TabTokenizer,
    LineTokenizer,
    line_tokenize,
)

from simple_nltk.tokenize.util import string_span_tokenize, regexp_span_tokenize


from simple_nltk.tokenize.api import TokenizerI
class NewlineTokenizer(TokenizerI):
    def tokenize(self, text):
        return text.splitlines()
def simple_sent_tokenize(text):
    """
    a simple version sentence tokenize, split sentence by \n
    """
    tokenizer = NewlineTokenizer()
    return tokenizer.tokenize(text)


# Standard word tokenizer.
_treebank_word_tokenizer = simple_nltkWordTokenizer()


def word_tokenize(text, language="english", preserve_line=False):
    """
    Return a tokenized copy of *text*,
    using simple_nltk's recommended word tokenizer
    (currently an improved :class:`.TreebankWordTokenizer`
    along with :class:`.PunktSentenceTokenizer`
    for the specified language).

    :param text: text to split into words
    :type text: str
    :param language: the model name in the Punkt corpus
    :type language: str
    :param preserve_line: An option to keep the preserve the sentence and not sentence tokenize it.
    :type preserve_line: bool
    """
    sentences = [text] if preserve_line else simple_sent_tokenize(text)
    return [
        token for sent in sentences for token in _treebank_word_tokenizer.tokenize(sent)
    ]
