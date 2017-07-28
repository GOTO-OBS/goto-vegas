# -*- coding: utf-8 -*-

from __future__ import division, print_function
import os
import requests
import shutil


paths = [
    ("training_set", "TRAINING_SET_URI_{0}"),
    ("test_set", "TEST_SET_URI_{0}")
]

for local_folder, environment_key in paths:

    if not os.path.exists(os.path.dirname(local_folder)):
        os.mkdir(os.path.dirname(local_folder))

    # Loop over and grab all relevant data.
    index = 0
    while True:
        remote_path = os.environ.get(environment_key.format(index))
        if remote_path is None: break

        response = requests.get(remote_path, stream=True)
        local_path = os.path.join(local_folder, os.path.basename(remote_path))
        with open(local_path, "wb") as fp:
            shutil.copyfileobj(response.raw, fp)
        del response

        print("Downloaded {}".format(local_path))

        if local_path.endswith(".gz"):
            os.system("gunzip -v {}".format(local_path))

        index += 1
