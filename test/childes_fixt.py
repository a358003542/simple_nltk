# -*- coding: utf-8 -*-


def setup_module(module):
    from nose import SkipTest
    import simple_nltk.data

    try:
        simple_nltk.data.find("corpora/childes/data-xml/Eng-USA-MOR/")
    except LookupError as e:
        print(e)
        raise SkipTest(
            "The CHILDES corpus is not found. "
            "It should be manually downloaded and saved/unpacked "
            "to [simple_nltk_Data_Dir]/corpora/childes/"
        )
