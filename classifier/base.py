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
        N_classified_correctly = 0
        N_misclassified = 10
        score = np.random.uniform(0, 1)

        return (N_classified_correctly, N_misclassified, score)

    