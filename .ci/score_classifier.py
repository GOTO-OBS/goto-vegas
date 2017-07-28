# -*- coding: utf-8 -*-

""" Score the classifier and update the local leaderboard. """

from __future__ import division, print_function
import inspect
import os
import requests
import sys
from astropy.table import Table, vstack
from datetime import datetime
from glob import glob
from time import time

cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.dirname(cwd))

from classifier import Classifier

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
training_set_paths = glob("training_set/*.csv")
if len(training_set_paths) == 0:
    print("No training set data")
    sys.exit(1)

training_set = vstack([
    Table.read(path, format="csv") for path in training_set_paths])
training_set_predictors = training_set[predictor_names]
training_set_classifications = (training_set["srctype"] == 1)

# Load the test set
test_set_paths = glob("test_set/*.csv")
if len(test_set_paths) == 0:
    print("No test set data")
    sys.exit(1)

test_set = vstack([
    Table.read(path, format="csv") for path in test_set_paths])
test_set_predictors = test_set[predictor_names]
test_set_classifications = (test_set["srctype"] == 1)

classifier = Classifier()

# Train the classifier.
t = time()
classifier.train(training_set_predictors, training_set_classifications)
t_train = time() - t

# Score the classifier.
t = time()
N_true_transients_found, N_true_transients_missed, N_false_positives, score \
    = classifier.score(test_set_predictors, test_set_classifications)
t_test = time() - t

# Prepare the entries row
human_readable = lambda t: "{:.0f}s".format(t) if t < 60 else "{:.0f}m {:.0f}s".format(t/60, t % 60)

entry = [
    datetime.now().strftime("%Y/%m/%d %I:%M:%s"), # now
    os.environ["TRAVIS_BRANCH"], # branch
    os.environ["TRAVIS_COMMIT"], # commit hash
    "https://github.com/goto-obs/goto-vegas/tree/{TRAVIS_BRANCH}".format(**os.environ), # branch_url
    "https://travis-ci.org/goto-obs/goto-vegas/builds/{TRAVIS_BUILD_ID}".format(**os.environ), # travis_url
    "https://github.com/goto-obs/goto-vegas/commit/{TRAVIS_COMMIT}".format(**os.environ), # commit_url
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
    .format(**os.environ))
with open("entries.csv", "w") as fp:
    fp.write("{}\n{}".format(response.content, ",".join(entry)))
del response


os.system("cat entries.csv")

entries = Table.read("entries.csv", format="csv")
entries.sort(keys=["score"])
entries = entries[::-1]

lb_header = """
| Rank | Time | Branch | Commit | Python | Train time | Test time | Transients found | Transients missed | False positives | Score |
|------|------|--------|--------|--------|------------|-----------|------------------|-------------------|-----------------|-------|
"""

lb_row_formatter = "|{rank}|[{time}]({travis_url})|[{branch}]({branch_url})|[{commit_hash}]({commit_url})|{python_version}|{train_time}|{test_time}|{num_transients_found}|{num_transients_missed}|{num_false_positives}|{score}|\n"

top10_by_score = lb_header
for rank, entry in enumerate(entries[:10], start=1):
    kwds = dict(rank=rank)
    kwds.update({k: entry[k] for k in entry.dtype.names})
    top10_by_score += lb_row_formatter.format(**kwds)

# Update the README.md
with open("README.md.template", "r") as fp:
    template = fp.read()

with open("README.md", "w") as fp:
    fp.write(template.format(top10_by_score=top10_by_score))
