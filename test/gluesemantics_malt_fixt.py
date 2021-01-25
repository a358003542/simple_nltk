# -*- coding: utf-8 -*-


def setup_module(module):
    from nose import SkipTest
    from simple_nltk.parse.malt import MaltParser

    try:
        depparser = MaltParser("maltparser-1.7.2")
    except LookupError:
        raise SkipTest("MaltParser is not available")
