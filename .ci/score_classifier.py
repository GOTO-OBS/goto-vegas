# -*- coding: utf-8 -*-

""" Score the classifier and update the remote leaderboard. """

from __future__ import division, print_function
import os
import requests
import shutil
from astropy.table import Table, vstack
from classifier import Classifier
from datetime import datetime
from glob import glob
from time import time

predictor_names = [
    "fpos2",
    "fneg2",
    "fpos3",
    "fneg3",
    "bkg",
    "bkgstd",
    "n2sig5",
    "n3sig5",
    "n2sig7",
    "n3sig7",
    "satfrac",
    "nsat5",
    "nsat7",
    "detsemi_a",
    "detsemi_b",
    "detsemi_ratio",
    "mag",
    "merr",
    "src-s2n",
    "fwhm",
    "rel-fwhm",
    "calsrc_mag",
    "calsrc_match",
    "photid",
    "x",
    "y",
    "score-validity",
    "score-nsat5",
    "score-nsat7",
    "score-fpos3",
    "score-fneg3",
    "score-src-s2n",
    "score-n2sig5",
    "score-n3sig5",
    "score-n2sig7",
    "score-n3sig7",
    "score-rel-fwhm",
    "score-axes-ratio",
    "score-hasid"
]

# Load all training set.
training_set = vstack([
    Table.read(path, format="csv") for path in glob("training_set/*.csv")])
training_set_predictors = training_set[predictor_names]
training_set_classifications = (training_set["srctype"] == 1)

# Load the test set
test_set = vstack([
    Table.read(path, format="csv") for path in glob("test_set/*.csv")])
test_set_predictors = test_set[predictor_names]
test_set_classifications = (test_set["srctype"] == 1)


# Train the classifier
classifier = Classifier()

t = time()
classifier.train(training_set_predictors, training_set_classifications)
t_train = time() - t

# Score the classifier.
# correct = true transients that you found
# missed = true transients that you missed
# misclassified = normal stars that you classified as transients
N_true_transients_found, N_true_transients_missed, N_false_positives, score \
    = classifier.score(test_set_predictors, test_set_classifications)
t_test = time() - t_train

# Prepare the entries row
human_readable = lambda t: "{:.0f}s".format(t) if t < 60 else "{:.0f}m {:.0f}s".format(t/60, t % 60)

entry = [
    datetime.now().strftime("%Y/%m/%d %I:%M:%s"), # now
    os.environ["TRAVIS_BRANCH"], # branch
    os.environ["TRAVIS_COMMIT"], # commit hash
    "https://github.com/{TRAVIS_REPO_SLUG}/tree/{TRAVIS_BRANCH}".format(**os.environ), # branch_url
    "https://travis-ci.org/{TRAVIS_REPO_SLUG}/builds/{TRAVIS_BUILD_ID}".format(**os.environ), # travis_url
    "https://github.com/{TRAVIS_REPO_SLUG}/commit/{TRAVIS_COMMIT}".format(**os.environ), # commit_url
    os.environ["TRAVIS_PYTHON_VERSION"], # python_version
    human_readable(t_train), # train_time
    human_readable(t_test), # test_time
    str(N_true_transients_found), 
    str(N_true_transients_missed),
    str(N_false_positives),
    "{:.3f}".format(score)
]

# Get the latest copy of entries.csv from GitHub, and update it with this entry
response = requests.get(
    "https://raw.githubusercontent.com/{TRAVIS_REPO_SLUG}/master/entries.csv"\
    .format(**os.environ), stream=True)

with open("entries.csv", "wb") as fp:
    shutil.copyfileobj(response.raw, fp)
    fp.write("\n{}".format(",".join(entry)))
del response


import os
os.system("cat entries.csv")

# Update the leaderboard on the README.md

# Commit the new README.md and entries.csv to GitHub



# [links to build]<datetime> | [links to branch]<branch_name> |  [links to commit]<commit hash> | <python version> | <t_train> | <t_test> | <score>


# Save the result
#result_row_format = \
#"{TRAVIS_REPO_SLUG}:{TRAVIS_BRANCH}





print("score_classifier.py updated")
