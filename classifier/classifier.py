# -*- coding: utf-8 -*-

from __future__ import division, print_function
from .base import BaseClassifier

import numpy as np

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
        return np.zeros(len(predictors))
