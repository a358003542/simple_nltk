# -*- coding: utf-8 -*-
"""
Unit tests for simple_nltk.tokenize.
See also simple_nltk/test/tokenize.doctest
"""


import unittest

from nose import SkipTest
from nose.tools import assert_equal

from simple_nltk.tokenize import (
    punkt,
    word_tokenize,
)


class TestTokenize(unittest.TestCase):
    def test_pad_asterisk(self):
        """
        Test padding of asterisk for word tokenization.
        """
        text = "This is a, *weird sentence with *asterisks in it."
        expected = ['This', 'is', 'a', ',', '*', 'weird', 'sentence', 
                    'with', '*', 'asterisks', 'in', 'it', '.']
        self.assertEqual(word_tokenize(text), expected)
        
    def test_pad_dotdot(self):
        """
        Test padding of dotdot* for word tokenization.
        """
        text = "Why did dotdot.. not get tokenized but dotdotdot... did? How about manydots....."
        expected = ['Why', 'did', 'dotdot', '..', 'not', 'get', 
                    'tokenized', 'but', 'dotdotdot', '...', 'did', '?', 
                    'How', 'about', 'manydots', '.....']
        self.assertEqual(word_tokenize(text), expected)


    def test_word_tokenize(self):
        """
        Test word_tokenize function
        """
        
        sentence = "The 'v', I've been fooled but I'll seek revenge."
        expected = ['The', "'", 'v', "'", ',', 'I', "'ve", 'been', 'fooled', 
                    'but', 'I', "'ll", 'seek', 'revenge', '.']
        self.assertEqual(word_tokenize(sentence), expected)
        
        sentence = "'v' 're'"
        expected = ["'", 'v', "'", "'re", "'"]
        self.assertEqual(word_tokenize(sentence), expected)

    def test_punkt_pair_iter(self):

        test_cases = [
            ('12', [('1', '2'), ('2', None)]),
            ('123', [('1', '2'), ('2', '3'), ('3', None)]),
            ('1234', [('1', '2'), ('2', '3'), ('3', '4'), ('4', None)]),
        ]

        for (test_input, expected_output) in test_cases:
            actual_output = [x for x in punkt._pair_iter(test_input)]

            assert_equal(actual_output, expected_output)

    def test_punkt_pair_iter_handles_stop_iteration_exception(self):
        # test input to trigger StopIteration from next()
        it = iter([])
        # call method under test and produce a generator
        gen = punkt._pair_iter(it)
        # unpack generator, ensure that no error is raised
        list(gen)

    def test_punkt_tokenize_words_handles_stop_iteration_exception(self):
        obj = punkt.PunktBaseClass()

        class TestPunktTokenizeWordsMock:
            def word_tokenize(self, s):
                return iter([])

        obj._lang_vars = TestPunktTokenizeWordsMock()
        # unpack generator, ensure that no error is raised
        list(obj._tokenize_words('test'))
