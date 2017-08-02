# -*- coding: utf-8 -*-

from __future__ import division, print_function
import numpy as np
from sklearn.metrics import fbeta_score

__all__ = ["BaseClassifier"]

class BaseClassifier(object):

    def __init__(self):
        return None

    def train(self, predictors, classifications, **kwargs):
        raise NotImplementedError("function should be overloaded by subclass")

    def classify(self, predictors, **kwargs):
        raise NotImplementedError("function should be overloaded by subclass")

    def score(self, predictors, true_classifications, **kwargs):
        """
        Score the classifier's performance.
        :param predictors:
            An :class:`astropy.table.Table` of possible predictors, where the
            number of rows is the number of objects in the validation set.
        :param true_classifications:
            An array of classifications for all objects in the validation set.
            This array should have the same length as the number of predictor
            rows.
        :returns:
            A four-length tuple containing the number of true transients found,
            the number of transients missed, the number of false positives,
            and the calculated score.
        """

        N = len(true_classifications)
        if len(predictors) != N:
            raise ValueError("number of predictor rows does not match "\
                             "number of classifications")

        classifications = self.classify(predictors).astype(int)
        is_transient = (classifications == 1)

        N_transients_found = np.sum(classifications[is_transient] == 1)
        N_transients_missed = np.sum(classifications[is_transient] == 0)
        N_false_positives = np.sum(classifications[~is_transient])
        score = fbeta_score(true_classifications, classifications, beta=2)

        return (
            N_transients_found,
            N_transients_missed,
            N_false_positives,
            score
        )