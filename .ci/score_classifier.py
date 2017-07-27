# -*- coding: utf-8 -*-

""" Score the classifier and record the entry. """

from __future__ import division, print_function
from astropy.table import Table
from classifier import Classifier


predictor_names = [
    "fpos2", "fneg2", "fpos3", "fneg3", "bkg", "bkgstd", 
    "n5sig2", "n5sig3", "n7sig2", "n7sig3", "n9sig2", "n9sig3", 
    "satfrac", "nsat5", "nsat7", "nsat9", "detsemi_a", "detsemi_b", 
    "detsemi_ratio", "mag", "merr", "src-s2n", "fwhm", "rel-fwhm", "catsrc_mag", 
    "catsrc_match", "photid", "ra", "dec", "x", "y", "score-validity", 
    "score-nsat5", "score-nsat7", "score-nsat9", "score-fpos3", "score-fneg3", 
    "score-src-s2n", "score-n5sig2", "score-n5sig3", "score-n7sig2", 
    "score-n7sig3", "score-n9sig2", "score-n9sig3", "score-rel-fwhm", 
    "score-axes-ratio", "score-hasid"]

# Load the training set and construct some predictors
training_set = Table.read("data/training_set.csv", format="csv")
training_set_predictors = training_set[predictor_names]
training_set_classifications = (training_set["srctype"] == 1)


# Load the test set
test_set = Table.read("data/test_set.csv", format="csv")
test_set_predictors = test_set[predictor_names]
test_set_classifications = (test_set["srctype"] == 1)


# Train the classifier
classifier = Classifier()
classifier.train(training_set_predictors, training_set_classifications)


# Score the classifier
N_classified_correctly, N_misclassified, score \
    = classifier.score(test_set_predictors, test_set_classifications)


# Save the result




print("score_classifier.py updated")
