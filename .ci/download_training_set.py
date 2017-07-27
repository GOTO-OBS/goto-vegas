# -*- coding: utf-8 -*-

from __future__ import division, print_function
import os
import requests
import shutil

local_path = "training_set.gz"

uri = os.environ.get("TRAINING_SET_URI")

if uri is not None:
    response = requests.get(uri, stream=True)
    with open(local_path, "wb") as fp:
        shutil.copyfileobj(response.raw, fp)
    del response

    os.system("gunzip -v {}".format(local_path))

else:
    print("No TRAINING_SET_URI environment variable")