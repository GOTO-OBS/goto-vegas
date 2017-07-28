# -*- coding: utf-8 -*-

""" Score the classifier and update the local leaderboard. """

from __future__ import division, print_function
import numpy as np
import os
import requests
import sys
from astropy.table import Table, vstack
from datetime import datetime
from glob import glob
from time import time

from classifier import Classifier


# Load all training set.
training_set_paths = glob("training_set/*.csv")
if len(training_set_paths) == 0:
    print("No training set data")
    sys.exit(1)


training_set = vstack([
    Table.read(path, format="csv") for path in training_set_paths])
training_set_classifications = (training_set["srctype"] == 1)
del training_set["srctype"]


# Load the test set
test_set_paths = glob("test_set/*.csv")
if len(test_set_paths) == 0:
    print("No test set data")
    sys.exit(1)

test_set = vstack([
    Table.read(path, format="csv") for path in test_set_paths])
test_set_classifications = (test_set["srctype"] == 1)
del test_set["srctype"]


classifier = Classifier()

# Train the classifier.
t = time()
classifier.train(training_set, training_set_classifications)
#t_train = time() - t
t_train = 128

# Score the classifier.
t = time()
N_true_transients_found, N_true_transients_missed, N_false_positives, score \
    = classifier.score(test_set, test_set_classifications)
t_test = time() - t


def human_readable_time(seconds):
    if seconds < 60:
        return "{:.0f}s".format(seconds)
    else:
        return "{:.0f}m {:.0f}s".format(seconds/60, seconds % 60)


# Print a summary.
print("""Summary:
    Number of true transients found: {0}
    Number of true transients missed: {1}
    Number of false positives: {2}
    Overall score: {3:.3f}

    Train time: {4}
    Test time: {5}""".format(
        N_true_transients_found, N_true_transients_missed, N_false_positives,
        score, human_readable_time(t_train), human_readable_time(t_test)))


# If we are on Travis, then do some things.
if os.environ.get("TRAVIS"):

    entry = [
        datetime.now().strftime("%Y/%m/%d %I:%M:%S"),
        os.environ["TRAVIS_BRANCH"],
        os.environ["TRAVIS_COMMIT"][:8],
        "https://github.com/goto-obs/goto-vegas/tree/{TRAVIS_BRANCH}"\
            .format(**os.environ),
        "https://travis-ci.org/GOTO-OBS/goto-vegas/builds/{TRAVIS_BUILD_ID}"\
            .format(**os.environ),
        "https://github.com/goto-obs/goto-vegas/commit/{TRAVIS_COMMIT}"\
            .format(**os.environ),
        os.environ["TRAVIS_PYTHON_VERSION"],
        human_readable_time(t_train),
        human_readable_time(t_test),
        str(N_true_transients_found),
        str(N_true_transients_missed),
        str(N_false_positives),
        "{:.3f}".format(score)
    ]

    # Get the latest copy of entries.csv from GitHub, and update it with this entry
    r = requests.get(
        "https://raw.githubusercontent.com/{TRAVIS_REPO_SLUG}/master/entries.csv"\
        .format(**os.environ))

    with open("entries.csv", "w") as fp:
        fp.write("{}\n{}".format(r.content.decode("utf-8"), ",".join(entry)))


    entries = Table.read("entries.csv", format="csv")
    indices = np.argsort(entries["score"])[::-1]
    entries = entries[indices]

    column_names = ["rank", "time", "branch", "commit", "train time",
                    "test time", "transients found", "transients missed",
                    "false positives", "score"]

    leaderboard_row = \
        "|{rank}|[{time}]({travis_url})|[{branch}]({branch_url})"\
        "|[{commit_hash}]({commit_url})|{train_time}|{test_time}"\
        "|{num_transients_found}|{num_transients_missed}"\
        "|{num_false_positives}|{score}|\n"

    leaderboard = "| {0} |\n|-{1}-|\n".format(
        " | ".join([c.title() for c in column_names]),
        "-|-".join(["-" * len(c) for c in column_names]))

    for rank, entry in enumerate(entries[:10], start=1):
        kwds = dict(rank=rank)
        kwds.update({k: entry[k] for k in entry.dtype.names})
        leaderboard += leaderboard_row.format(**kwds)

    # Update the README.md
    with open("README.md.template", "r") as fp:
        template = fp.read()

        with open("README.md", "w") as fp:
            fp.write(template.format(top10_by_score=leaderboard))
