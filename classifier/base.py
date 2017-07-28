# -*- coding: utf-8 -*-

from __future__ import division, print_function
import numpy as np

__all__ = ["BaseClassifier"]

class BaseClassifier(object):

    def __init__(self):
        return None


    def train(self, predictors, classifications, **kwargs):
        return None

    def score(self, predictors, classifications, **kwargs):
        N_true_transients_found = 0
        N_true_transients_missed = 1
        N_false_positives = 10
        score = np.random.uniform(0, 1)

        return (
            N_true_transients_found, 
            N_true_transients_missed,
            N_false_positives,
            score
        )

    