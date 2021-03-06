# -*- coding: utf-8 -*-


def setup_module(module):
    from nose import SkipTest
    from simple_nltk.inference.mace import Mace

    try:
        m = Mace()
        m._find_binary("mace4")
    except LookupError:
        raise SkipTest(
            "Mace4/Prover9 is not available so inference.doctest was skipped"
        )
