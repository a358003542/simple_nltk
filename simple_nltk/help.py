# Natural Language Toolkit (simple_nltk) Help
#
# Copyright (C) 2001-2020 simple_nltk Project
# Authors: Steven Bird <stevenbird1@gmail.com>
# URL: <http://simple_nltk.org/>
# For license information, see LICENSE.TXT

"""
Provide structured access to documentation.
"""

import re
from textwrap import wrap



#####################################################################
# UTILITIES
#####################################################################


def _print_entries(tags, tagdict):
    for tag in tags:
        entry = tagdict[tag]
        defn = [tag + ": " + entry[0]]
        examples = wrap(
            entry[1], width=75, initial_indent="    ", subsequent_indent="    "
        )
        print("\n".join(defn + examples))

