# -*- coding: utf-8 -*-

from __future__ import division, print_function
import os
import requests
import shutil


urls = [
    (os.environ.get("TRAINING_SET_URI"), "data/training_set.gz"),
    (os.environ.get("TEST_SET_URI"), "data/test_set.gz")
]

for remote_path, local_path in urls:

    if remote_path is None:
        print("Cannot download file {}".format(local_path))
        continue

    if not os.path.exists(os.path.dirname(local_path)):
        os.mkdir(os.path.dirname(local_path))


    response = requests.get(remote_path, stream=True)
    with open(local_path, "wb") as fp:
        shutil.copyfileobj(response.raw, fp)
    del response

    os.system("gunzip -v {}".format(local_path))
