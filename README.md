[![Build Status](https://travis-ci.org/GOTO-OBS/goto-vegas.svg?branch=master)](https://travis-ci.org/GOTO-OBS/goto-vegas)

# GOTO Vegas
Classify transient sources accurately and efficiently.


# Leaderboard
| Rank | Time | Branch | Commit | Train Time | Test Time | Transients Found | Transients Missed | False Positives | Score |
|------|------|--------|--------|------------|-----------|------------------|-------------------|-----------------|-------|
|1|[17/07/30 07:40](https://travis-ci.org/GOTO-OBS/goto-vegas/builds/259036213)|[baseline](https://github.com/goto-obs/goto-vegas/tree/baseline)|[5f91179e](https://github.com/goto-obs/goto-vegas/commit/5f91179ecd1fd825be71dc205a1881d0c45e21d8)|0s|13s|56|39|56|0.569|



# Submit a classifier for evaluation
Any member of the [GOTO organization on GitHub](https://github.com/GOTO-OBS) can 
submit an entry. First, clone this repository and create a branch with a 
representative name (e.g., something like `<last_name>-<short_description>`) 
and switch to that branch:

```
git clone git@github.com:goto-obs/goto-vegas.git
cd goto-vegas
git branch casey-random-forest
git checkout casey-random-forest
```

Now create your classifier by changing the behaviour of the `Classifier` class
in [`classifier/classifier.py`](classifier/classifier.py). Specifically, you
will want to change the code in the `train` and `classify` functions.

Here is the worst kind of classifier, which will never find any transient:

```python
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
```

To submit your entry to the leaderboard, you will need to commit your changes and
push them to GitHub:

```
git add classifier/classifier.py
git commit -m "Add Random Forest entry"
git push --set-upstream origin casey-random-forest
```

Your classifier will be run on the test set and scored automatically by Travis CI.
Once the classifier has been scored, your entry will (hopefully!) appear on the
leaderboard. Otherwise, your classifier might have done a very bad job and not made
it in to the top ten. All entries evaluated by Travis CI are [available here](entries.csv).

Maintainer
----------
- [Andrew R. Casey](http://astrowizici.st) (Monash)
