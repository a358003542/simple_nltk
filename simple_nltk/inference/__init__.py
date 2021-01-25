# Natural Language Toolkit: Inference
#
# Copyright (C) 2001-2020 simple_nltk Project
# Author: Dan Garrette <dhgarrette@gmail.com>
#         Ewan Klein <ewan@inf.ed.ac.uk>
#
# URL: <http://simple_nltk.org/>
# For license information, see LICENSE.TXT

"""
Classes and interfaces for theorem proving and model building.
"""

from simple_nltk.inference.api import ParallelProverBuilder, ParallelProverBuilderCommand
from simple_nltk.inference.mace import Mace, MaceCommand
from simple_nltk.inference.prover9 import Prover9, Prover9Command
from simple_nltk.inference.resolution import ResolutionProver, ResolutionProverCommand
from simple_nltk.inference.tableau import TableauProver, TableauProverCommand
from simple_nltk.inference.discourse import (
    ReadingCommand,
    CfgReadingCommand,
    DrtGlueReadingCommand,
    DiscourseTester,
)
