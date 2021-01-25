# Natural Language Toolkit: Metrics
#
# Copyright (C) 2001-2020 simple_nltk Project
# Author: Steven Bird <stevenbird1@gmail.com>
#         Edward Loper <edloper@gmail.com>
# URL: <http://simple_nltk.org/>
# For license information, see LICENSE.TXT
#

"""
simple_nltk Metrics

Classes and methods for scoring processing modules.
"""

from simple_nltk.metrics.scores import (
    accuracy,
    precision,
    recall,
    f_measure,
    log_likelihood,
    approxrand,
)
from simple_nltk.metrics.confusionmatrix import ConfusionMatrix
from simple_nltk.metrics.distance import (
    edit_distance,
    edit_distance_align,
    binary_distance,
    jaccard_distance,
    masi_distance,
    interval_distance,
    custom_distance,
    presence,
    fractional_presence,
)
from simple_nltk.metrics.paice import Paice
from simple_nltk.metrics.segmentation import windowdiff, ghd, pk
from simple_nltk.metrics.agreement import AnnotationTask
from simple_nltk.metrics.association import (
    NgramAssocMeasures,
    BigramAssocMeasures,
    TrigramAssocMeasures,
    QuadgramAssocMeasures,
    ContingencyMeasures,
)
from simple_nltk.metrics.spearman import (
    spearman_correlation,
    ranks_from_sequence,
    ranks_from_scores,
)
