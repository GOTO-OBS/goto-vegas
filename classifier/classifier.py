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
        Classify a single object, given some predictors.

        :param predictors:
            A row of predictors for a single object.

        :returns:
            A single-valued classification for this object.
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

        score = {}
        score["hasid"] = (predictors["photid"] > 0).astype(int)
        if predictors["nsat5"] > 5:
            score["nsat5"] = -0.5
        elif predictors["nsat5"] > 2:
            score["nsat5"] = -0.2

        if predictors["nsat7"] > 15:
            score["nsat7"] = -1

        if predictors["fneg3"] < 0.01:
            score["fneg3"] = 0.5

        elif predictors["fneg3"] < 0.1:
            score["fneg3"] = 0.2

        if predictors["src-s2n"] > 50:
            score["src-s2n"] = 0.5

        if predictors["n2sig5"] <= 2:
            score["n2sig5"] = 0.5

        if predictors["n2sig7"] <= 2:
            score["n2sig7"] = 0.5

        if predictors["n3sig5"] <= 2:
            score["n3sig5"] = 0.5

        score["n3sig7"] = np.exp(-predictors["n3sig7"]/10.0) - 1.0

        weighted_score = 0
        for key, weight in weights.items():
            weighted_score += score.get(key, 0) * weight

        weighted_score /= sum(weights.values())

        # Added some cut.
        return (weighted_score > 0.23).astype(int)
