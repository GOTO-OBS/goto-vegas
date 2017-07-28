[![Build Status](https://travis-ci.org/GOTO-OBS/goto-vegas.svg?branch=master)](https://travis-ci.org/GOTO-OBS/goto-vegas)

# GOTO Vegas
Classify transient sources accurately and efficiently.


# Leaderboard
| Rank | Time | Branch | Commit | Train Time | Test Time | Transients Found | Transients Missed | False Positives | Score |
|------|------|--------|--------|------------|-----------|------------------|-------------------|-----------------|-------|
|1|[2017/07/28 11:35:15](https://travis-ci.org/goto-obs/goto-vegas/builds/258519388)|[master](https://github.com/goto-obs/goto-vegas/tree/master)|[964410dc](https://github.com/goto-obs/goto-vegas/commit/964410dcaf9d96559ef819c21f0e42e764920650)|0s|0s|19334|3955|4349|0.94|
|2|[2017/07/28 11:43:28](https://travis-ci.org/GOTO-OBS/goto-vegas/builds/258522008)|[master](https://github.com/goto-obs/goto-vegas/tree/master)|[53b1ff77](https://github.com/goto-obs/goto-vegas/commit/53b1ff77323a3bd6d16205c105196bde2e211ab0)|0s|0s|10715|6783|1768|0.29|



# Submit a classifier for evaluation
Any member of the [GOTO organization on GitHub](https://github.com/GOTO-OBS) can 
submit an entry. First, clone this repository and create a branch with a 
representative name (e.g., something like ``<last_name>-<short_description>``) 
and switch to that branch:

````
git clone git@github.com:goto-obs/goto-vegas.git
cd goto-vegas
git branch casey-random-forest
git checkout casey-random-forest
````

Now create your classifier by changing the behaviour of the ``Classifier`` class
in [``classifier/classifier.py``](classifier/classifier.py). Specifically, you
will want to change the code in the ``train`` and ``classify`` functions.

Here is the worst kind of classifier, which will never find any transient:

````python
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
            This array should have the same length as the number of predictor rows.
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
````

To submit your entry to the leaderboard, you will need to commit your changes and
push them to GitHub:

````
git add classifier/classifier.py
git commit -m "Add Random Forest entry"
git push origin
````

Your classifier will be run on the test set and scored automatically by Travis CI.
Once the classifier has been scored, your entry will (hopefully!) appear on the
leaderboard. Otherwise, your classifier might have done a very bad job and not made
it in to the top ten. All entries evaluated by Travis CI are [available here](entries.csv).

Maintainer
----------
- Andrew R. Casey (Monash)
