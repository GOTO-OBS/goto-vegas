# -*- coding: utf-8 -*-

from __future__ import division, print_function
from .base import BaseClassifier
import numpy as np
from sklearn.ensemble import RandomForestClassifier


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

        df = predictors.to_pandas()  #  RFC doesn't like Astropy tables
        df = df.fillna(0)  # RCS doesn't like NaNs.
                           # Potentially, a different (large, negative?)
                           # value may be better. To test and find out
        self.clf = RandomForestClassifier(n_estimators=100, max_features='sqrt',
                                          n_jobs=4, class_weight='balanced')
        self.clf.fit(df, classifications)

        return None


    def classify(self, predictors, **kwargs):
        """
        Classify a single object, given some predictors.

        :param predictors:
            A row of predictors for a single object.

        :returns:
            A single-valued classification for this object.
        """

        data = np.array(predictors.as_void().tolist()).reshape(1, -1)
        return self.clf.predict(data)
