# -*- coding: utf-8 -*-
from simple_nltk.corpus import teardown_module


def setup_module(module):
    from nose import SkipTest

    raise SkipTest(
        "portuguese_en.doctest imports simple_nltk.examples.pt which doesn't exist!"
    )
