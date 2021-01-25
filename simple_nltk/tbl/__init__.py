# -*- coding: utf-8 -*-
# Natural Language Toolkit: Transformation-based learning
#
# Copyright (C) 2001-2020 simple_nltk Project
# Author: Marcus Uneson <marcus.uneson@gmail.com>
#   based on previous (simple_nltk2) version by
#   Christopher Maloof, Edward Loper, Steven Bird
# URL: <http://simple_nltk.org/>
# For license information, see  LICENSE.TXT

"""
Transformation Based Learning

A general purpose package for Transformation Based Learning,
currently used by simple_nltk.tag.BrillTagger.
"""

from simple_nltk.tbl.template import Template

# API: Template(...), Template.expand(...)

from simple_nltk.tbl.feature import Feature

# API: Feature(...), Feature.expand(...)

from simple_nltk.tbl.rule import Rule

# API: Rule.format(...), Rule.templatetid

from simple_nltk.tbl.erroranalysis import error_list
