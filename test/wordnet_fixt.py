# -*- coding: utf-8 -*-


def teardown_module(module=None):
    from simple_nltk.corpus import wordnet

    wordnet._unload()
