# coding: utf-8
#
# Natural Language Toolkit: Sentiment Analyzer
#
# Copyright (C) 2001-2020 simple_nltk Project
# Author: Pierpaolo Pantone <24alsecondo@gmail.com>
# URL: <http://simple_nltk.org/>
# For license information, see LICENSE.TXT

"""
Utility methods for Sentiment Analysis.
"""

import codecs
import csv
import json
import pickle
import random
import re
import sys
import time
from copy import deepcopy

import simple_nltk
from simple_nltk.corpus import CategorizedPlaintextCorpusReader
from simple_nltk.data import load

# ////////////////////////////////////////////////////////////
# { Regular expressions
# ////////////////////////////////////////////////////////////

# Regular expression for negation by Christopher Potts
NEGATION = r"""
    (?:
        ^(?:never|no|nothing|nowhere|noone|none|not|
            havent|hasnt|hadnt|cant|couldnt|shouldnt|
            wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint
        )$
    )
    |
    n't"""

NEGATION_RE = re.compile(NEGATION, re.VERBOSE)

CLAUSE_PUNCT = r"^[.:;!?]$"
CLAUSE_PUNCT_RE = re.compile(CLAUSE_PUNCT)

# Happy and sad emoticons

HAPPY = set(
    [
        ":-)",
        ":)",
        ";)",
        ":o)",
        ":]",
        ":3",
        ":c)",
        ":>",
        "=]",
        "8)",
        "=)",
        ":}",
        ":^)",
        ":-D",
        ":D",
        "8-D",
        "8D",
        "x-D",
        "xD",
        "X-D",
        "XD",
        "=-D",
        "=D",
        "=-3",
        "=3",
        ":-))",
        ":'-)",
        ":')",
        ":*",
        ":^*",
        ">:P",
        ":-P",
        ":P",
        "X-P",
        "x-p",
        "xp",
        "XP",
        ":-p",
        ":p",
        "=p",
        ":-b",
        ":b",
        ">:)",
        ">;)",
        ">:-)",
        "<3",
    ]
)

SAD = set(
    [
        ":L",
        ":-/",
        ">:/",
        ":S",
        ">:[",
        ":@",
        ":-(",
        ":[",
        ":-||",
        "=L",
        ":<",
        ":-[",
        ":-<",
        "=\\",
        "=/",
        ">:(",
        ":(",
        ">.<",
        ":'-(",
        ":'(",
        ":\\",
        ":-c",
        ":c",
        ":{",
        ">:\\",
        ";(",
    ]
)


def timer(method):
    """
    A timer decorator to measure execution performance of methods.
    """

    def timed(*args, **kw):
        start = time.time()
        result = method(*args, **kw)
        end = time.time()
        tot_time = end - start
        hours = tot_time // 3600
        mins = tot_time // 60 % 60
        # in Python 2.x round() will return a float, so we convert it to int
        secs = int(round(tot_time % 60))
        if hours == 0 and mins == 0 and secs < 10:
            print("[TIMER] {0}(): {:.3f} seconds".format(method.__name__, tot_time))
        else:
            print(
                "[TIMER] {0}(): {1}h {2}m {3}s".format(
                    method.__name__, hours, mins, secs
                )
            )
        return result

    return timed


# ////////////////////////////////////////////////////////////
# { Feature extractor functions
# ////////////////////////////////////////////////////////////
"""
Feature extractor functions are declared outside the SentimentAnalyzer class.
Users should have the possibility to create their own feature extractors
without modifying SentimentAnalyzer.
"""


def extract_unigram_feats(document, unigrams, handle_negation=False):
    """
    Populate a dictionary of unigram features, reflecting the presence/absence in
    the document of each of the tokens in `unigrams`.

    :param document: a list of words/tokens.
    :param unigrams: a list of words/tokens whose presence/absence has to be
        checked in `document`.
    :param handle_negation: if `handle_negation == True` apply `mark_negation`
        method to `document` before checking for unigram presence/absence.
    :return: a dictionary of unigram features {unigram : boolean}.

    >>> words = ['ice', 'police', 'riot']
    >>> document = 'ice is melting due to global warming'.split()
    >>> sorted(extract_unigram_feats(document, words).items())
    [('contains(ice)', True), ('contains(police)', False), ('contains(riot)', False)]
    """
    features = {}
    if handle_negation:
        document = mark_negation(document)
    for word in unigrams:
        features["contains({0})".format(word)] = word in set(document)
    return features


def extract_bigram_feats(document, bigrams):
    """
    Populate a dictionary of bigram features, reflecting the presence/absence in
    the document of each of the tokens in `bigrams`. This extractor function only
    considers contiguous bigrams obtained by `simple_nltk.bigrams`.

    :param document: a list of words/tokens.
    :param unigrams: a list of bigrams whose presence/absence has to be
        checked in `document`.
    :return: a dictionary of bigram features {bigram : boolean}.

    >>> bigrams = [('global', 'warming'), ('police', 'prevented'), ('love', 'you')]
    >>> document = 'ice is melting due to global warming'.split()
    >>> sorted(extract_bigram_feats(document, bigrams).items())
    [('contains(global - warming)', True), ('contains(love - you)', False),
    ('contains(police - prevented)', False)]
    """
    features = {}
    for bigr in bigrams:
        features["contains({0} - {1})".format(bigr[0], bigr[1])] = bigr in simple_nltk.bigrams(
            document
        )
    return features


# ////////////////////////////////////////////////////////////
# { Helper Functions
# ////////////////////////////////////////////////////////////


def mark_negation(document, double_neg_flip=False, shallow=False):
    """
    Append _NEG suffix to words that appear in the scope between a negation
    and a punctuation mark.

    :param document: a list of words/tokens, or a tuple (words, label).
    :param shallow: if True, the method will modify the original document in place.
    :param double_neg_flip: if True, double negation is considered affirmation
        (we activate/deactivate negation scope everytime we find a negation).
    :return: if `shallow == True` the method will modify the original document
        and return it. If `shallow == False` the method will return a modified
        document, leaving the original unmodified.

    >>> sent = "I didn't like this movie . It was bad .".split()
    >>> mark_negation(sent)
    ['I', "didn't", 'like_NEG', 'this_NEG', 'movie_NEG', '.', 'It', 'was', 'bad', '.']
    """
    if not shallow:
        document = deepcopy(document)
    # check if the document is labeled. If so, do not consider the label.
    labeled = document and isinstance(document[0], (tuple, list))
    if labeled:
        doc = document[0]
    else:
        doc = document
    neg_scope = False
    for i, word in enumerate(doc):
        if NEGATION_RE.search(word):
            if not neg_scope or (neg_scope and double_neg_flip):
                neg_scope = not neg_scope
                continue
            else:
                doc[i] += "_NEG"
        elif neg_scope and CLAUSE_PUNCT_RE.search(word):
            neg_scope = not neg_scope
        elif neg_scope and not CLAUSE_PUNCT_RE.search(word):
            doc[i] += "_NEG"

    return document


def output_markdown(filename, **kwargs):
    """
    Write the output of an analysis to a file.
    """
    with codecs.open(filename, "at") as outfile:
        text = "\n*** \n\n"
        text += "{0} \n\n".format(time.strftime("%d/%m/%Y, %H:%M"))
        for k in sorted(kwargs):
            if isinstance(kwargs[k], dict):
                dictionary = kwargs[k]
                text += "  - **{0}:**\n".format(k)
                for entry in sorted(dictionary):
                    text += "    - {0}: {1} \n".format(entry, dictionary[entry])
            elif isinstance(kwargs[k], list):
                text += "  - **{0}:**\n".format(k)
                for entry in kwargs[k]:
                    text += "    - {0}\n".format(entry)
            else:
                text += "  - **{0}:** {1} \n".format(k, kwargs[k])
        outfile.write(text)


def split_train_test(all_instances, n=None):
    """
    Randomly split `n` instances of the dataset into train and test sets.

    :param all_instances: a list of instances (e.g. documents) that will be split.
    :param n: the number of instances to consider (in case we want to use only a
        subset).
    :return: two lists of instances. Train set is 8/10 of the total and test set
        is 2/10 of the total.
    """
    random.seed(12345)
    random.shuffle(all_instances)
    if not n or n > len(all_instances):
        n = len(all_instances)
    train_set = all_instances[: int(0.8 * n)]
    test_set = all_instances[int(0.8 * n) : n]

    return train_set, test_set


def _show_plot(x_values, y_values, x_labels=None, y_labels=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError(
            "The plot function requires matplotlib to be installed."
            "See http://matplotlib.org/"
        )

    plt.locator_params(axis="y", nbins=3)
    axes = plt.axes()
    axes.yaxis.grid()
    plt.plot(x_values, y_values, "ro", color="red")
    plt.ylim(ymin=-1.2, ymax=1.2)
    plt.tight_layout(pad=5)
    if x_labels:
        plt.xticks(x_values, x_labels, rotation="vertical")
    if y_labels:
        plt.yticks([-1, 0, 1], y_labels, rotation="horizontal")
    # Pad margins so that markers are not clipped by the axes
    plt.margins(0.2)
    plt.show()




# ////////////////////////////////////////////////////////////
# { Demos
# ////////////////////////////////////////////////////////////

def demo_movie_reviews(trainer, n_instances=None, output=None):
    """
    Train classifier on all instances of the Movie Reviews dataset.
    The corpus has been preprocessed using the default sentence tokenizer and
    WordPunctTokenizer.
    Features are composed of:
        - most frequent unigrams

    :param trainer: `train` method of a classifier.
    :param n_instances: the number of total reviews that have to be used for
        training and testing. Reviews will be equally split between positive and
        negative.
    :param output: the output file where results have to be reported.
    """
    from simple_nltk.corpus import movie_reviews
    from simple_nltk.sentiment import SentimentAnalyzer

    if n_instances is not None:
        n_instances = int(n_instances / 2)

    pos_docs = [
        (list(movie_reviews.words(pos_id)), "pos")
        for pos_id in movie_reviews.fileids("pos")[:n_instances]
    ]
    neg_docs = [
        (list(movie_reviews.words(neg_id)), "neg")
        for neg_id in movie_reviews.fileids("neg")[:n_instances]
    ]
    # We separately split positive and negative instances to keep a balanced
    # uniform class distribution in both train and test sets.
    train_pos_docs, test_pos_docs = split_train_test(pos_docs)
    train_neg_docs, test_neg_docs = split_train_test(neg_docs)

    training_docs = train_pos_docs + train_neg_docs
    testing_docs = test_pos_docs + test_neg_docs

    sentim_analyzer = SentimentAnalyzer()
    all_words = sentim_analyzer.all_words(training_docs)

    # Add simple unigram word features
    unigram_feats = sentim_analyzer.unigram_word_feats(all_words, min_freq=4)
    sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
    # Apply features to obtain a feature-value representation of our datasets
    training_set = sentim_analyzer.apply_features(training_docs)
    test_set = sentim_analyzer.apply_features(testing_docs)

    classifier = sentim_analyzer.train(trainer, training_set)
    try:
        classifier.show_most_informative_features()
    except AttributeError:
        print(
            "Your classifier does not provide a show_most_informative_features() method."
        )
    results = sentim_analyzer.evaluate(test_set)

    if output:
        extr = [f.__name__ for f in sentim_analyzer.feat_extractors]
        output_markdown(
            output,
            Dataset="Movie_reviews",
            Classifier=type(classifier).__name__,
            Tokenizer="WordPunctTokenizer",
            Feats=extr,
            Results=results,
            Instances=n_instances,
        )


def demo_subjectivity(trainer, save_analyzer=False, n_instances=None, output=None):
    """
    Train and test a classifier on instances of the Subjective Dataset by Pang and
    Lee. The dataset is made of 5000 subjective and 5000 objective sentences.
    All tokens (words and punctuation marks) are separated by a whitespace, so
    we use the basic WhitespaceTokenizer to parse the data.

    :param trainer: `train` method of a classifier.
    :param save_analyzer: if `True`, store the SentimentAnalyzer in a pickle file.
    :param n_instances: the number of total sentences that have to be used for
        training and testing. Sentences will be equally split between positive
        and negative.
    :param output: the output file where results have to be reported.
    """
    from simple_nltk.sentiment import SentimentAnalyzer
    from simple_nltk.corpus import subjectivity

    if n_instances is not None:
        n_instances = int(n_instances / 2)

    subj_docs = [
        (sent, "subj") for sent in subjectivity.sents(categories="subj")[:n_instances]
    ]
    obj_docs = [
        (sent, "obj") for sent in subjectivity.sents(categories="obj")[:n_instances]
    ]

    # We separately split subjective and objective instances to keep a balanced
    # uniform class distribution in both train and test sets.
    train_subj_docs, test_subj_docs = split_train_test(subj_docs)
    train_obj_docs, test_obj_docs = split_train_test(obj_docs)

    training_docs = train_subj_docs + train_obj_docs
    testing_docs = test_subj_docs + test_obj_docs

    sentim_analyzer = SentimentAnalyzer()
    all_words_neg = sentim_analyzer.all_words(
        [mark_negation(doc) for doc in training_docs]
    )

    # Add simple unigram word features handling negation
    unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
    sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

    # Apply features to obtain a feature-value representation of our datasets
    training_set = sentim_analyzer.apply_features(training_docs)
    test_set = sentim_analyzer.apply_features(testing_docs)

    classifier = sentim_analyzer.train(trainer, training_set)
    try:
        classifier.show_most_informative_features()
    except AttributeError:
        print(
            "Your classifier does not provide a show_most_informative_features() method."
        )
    results = sentim_analyzer.evaluate(test_set)

    if save_analyzer == True:
        save_file(sentim_analyzer, "sa_subjectivity.pickle")

    if output:
        extr = [f.__name__ for f in sentim_analyzer.feat_extractors]
        output_markdown(
            output,
            Dataset="subjectivity",
            Classifier=type(classifier).__name__,
            Tokenizer="WhitespaceTokenizer",
            Feats=extr,
            Instances=n_instances,
            Results=results,
        )

    return sentim_analyzer


def demo_sent_subjectivity(text):
    """
    Classify a single sentence as subjective or objective using a stored
    SentimentAnalyzer.

    :param text: a sentence whose subjectivity has to be classified.
    """
    from simple_nltk.classify import NaiveBayesClassifier
    from simple_nltk.tokenize import regexp

    word_tokenizer = regexp.WhitespaceTokenizer()
    try:
        sentim_analyzer = load("sa_subjectivity.pickle")
    except LookupError:
        print("Cannot find the sentiment analyzer you want to load.")
        print("Training a new one using NaiveBayesClassifier.")
        sentim_analyzer = demo_subjectivity(NaiveBayesClassifier.train, True)

    # Tokenize and convert to lower case
    tokenized_text = [word.lower() for word in word_tokenizer.tokenize(text)]
    print(sentim_analyzer.classify(tokenized_text))



def demo_vader_instance(text):
    """
    Output polarity scores for a text using Vader approach.

    :param text: a text whose polarity has to be evaluated.
    """
    from simple_nltk.sentiment import SentimentIntensityAnalyzer

    vader_analyzer = SentimentIntensityAnalyzer()
    print(vader_analyzer.polarity_scores(text))



if __name__ == "__main__":
    from simple_nltk.classify import NaiveBayesClassifier, MaxentClassifier
    from simple_nltk.classify.scikitlearn import SklearnClassifier

    naive_bayes = NaiveBayesClassifier.train
    maxent = MaxentClassifier.train

    # demo_movie_reviews(svm)
    # demo_subjectivity(svm)
    # demo_sent_subjectivity("she's an artist , but hasn't picked up a brush in a year . ")
    # demo_liu_hu_lexicon("This movie was actually neither that funny, nor super witty.", plot=True)
    # demo_vader_instance("This movie was actually neither that funny, nor super witty.")
    # demo_vader_tweets()
