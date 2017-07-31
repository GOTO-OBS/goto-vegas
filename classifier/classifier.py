# -*- coding: utf-8 -*-

from __future__ import division, print_function
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
        return 0


    def vclassify(self, predictors, **kwargs):
        """
        Classify a list of objects, given some predictors.

        This classifier method takes precedence over `self.classify`,
        provided it exists and is implemented.

        This method is optional: if it's not implemented (or simply
        does not exist), the classification is calculated by looping
        over the classify method.

        :param predictors:
            An :class:`astropy.table.Table` of objects (rows) with
            their predictors (columns).

        :returns:
            An array of classifications (0 or 1 integers) for the
            input objects.
        """
        raise NotImplementedError
        #return np.zeros(len(predictors), dtype=np.int)
