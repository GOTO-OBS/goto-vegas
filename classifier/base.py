# -*- coding: utf-8 -*-

from __future__ import division, print_function
import numpy as np

__all__ = ["BaseClassifier"]

class BaseClassifier(object):

    def __init__(self):
        return None

    def train(self, predictors, classifications, **kwargs):
        raise NotImplementedError("function should be overloaded by subclass")

    def classify(self, predictors, **kwargs):
        raise NotImplementedError("function should be overloaded by subclass")

    def score(self, predictors, classifications, **kwargs):
        """
        Score the classifier's performance.

        :param predictors:
            An :class:`astropy.table.Table` of possible predictors, where the
            number of rows is the number of objects in the validation set.
           
        :param classifications:
            An array of classifications for all objects in the validation set.
            This array should have the same length as the number of predictor 
            rows.

        :returns:
            A four-length tuple containing the number of true transients found,
            the number of transients missed, the number of false positives, 
            and the calculated score.
        """

        N_true_transients_found = np.random.randint(high=len(predictors)/3)
        N_true_transients_missed = np.random.randint(high=len(predictors)/3)
        N_false_positives = np.random.randint(high=len(predictors)/3)
        score = np.random.uniform(0, 1)

        return (
            N_true_transients_found, 
            N_true_transients_missed,
            N_false_positives,
            score
        )

    