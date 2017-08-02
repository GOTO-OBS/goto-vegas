# -*- coding: utf-8 -*-

from __future__ import division, print_function
import numpy as np
from .base import BaseClassifier

class Classifier(BaseClassifier):

    def train(self, predictors, classifications, **kwargs):
        """
        Train the model based on a table of predictors and known classifications
        for objects in a training set.

        :param predictors:
            An :class:`astropy.table.Table` of possible predictors, where the
            number of rows is the number of objects in the training set.

        :param classifications:
            An array of classifications for all objects in the training set.
            This array should have the same length as the number of predictor
            rows.
        """
        return None


    def classify(self, predictors, **kwargs):
        """
        Classify multiple objects, given the predictors for each object.

        :param predictors:
            A table of predictors (one row per object).

        :returns:
            A single-valued classification for each object.
        """

        weights = {
            "fpos3": 2,
            "nsat5": 2,
            "nsat7": 1,
            "fneg3": 1,
            "n3sig7": 2,
            "src-s2n": 0.5,
            "hasid": 2
        }

        N = len(predictors)
        scores = dict([(k, np.zeros(N, dtype=float)) for k in weights.keys()])
        
        scores["hasid"] = (predictors["photid"] > 0).astype(int)

        scores["nsat5"][predictors["nsat5"] > 2] = -0.2
        scores["nsat5"][predictors["nsat5"] > 5] = -0.5
        scores["nsat7"][predictors["nsat7"] > 15] = -1
        scores["fneg3"][predictors["fneg3"] < 0.01] = 0.5
        scores["fneg3"][predictors["fneg3"] < 0.1] = 0.2
        scores["src-s2n"][predictors["src-s2n"] > 50] = 0.5
        #scores["n2sig5"][predictors["n2sig5"] <= 2] = 0.5
        #scores["n2sig7"][predictors["n2sig7"] <= 2] = 0.5
        #scores["n3sig5"][predictors["n3sig5"] <= 2] = 0.5
        scores["n3sig7"] = np.exp(-predictors["n3sig7"]/10.0) - 1.0

        weighted_scores = np.zeros(N)
        for key, weight in weights.items():
            weighted_scores += scores[key] * weight

        weighted_scores /= sum(weights.values())

        # Added some threshold
        return (weighted_scores > 0.23).astype(int)
