import os
for i in range(7):
    print(os.environ.get("TRAINING_SET_URI_{:.0f}".format(i)))
