GOTO Vegas
----------
Classify transient sources, and throw away the junk.


Leaderboard
-----------
{top10_by_score}


Submit an entry
---------------
Any member of the GOTO organization on GitHub can submit an entry. First, clone this 
repository and create a branch with a representative name (e.g., something like 
``<last_name>-<short_description>``) and switch to that branch.

````
git clone git@github.com:goto-obs/goto-vegas.git
cd goto-vegas
git branch casey-random-forest
git checkout casey-random-forest
````

Now create your classifier by changing the behaviour of the ``Classifier`` class
in ``classifier.py`` (TODO)

[test performance locally]

To submit your entry to the leaderboard, you will need to commit your changes and
push them to GitHub:

````
git add classifier.py
git commit -m "Add Random Forest entry"
git push origin
````

Your classifier will be run on the test set and scored automatically by Travis CI.
Once the classifier has been scored, your entry will (hopefully!) appear on the
leaderboard. Otherwise, your classifier might have done a very bad job and not made
it in to the top ten. All entries evaluated by Travis CI are [available here](entries.csv).

Authors
-------
- Andrew R. Casey (Monash)
- Duncan Galloway (Monash)
- Evert Rol (Monash)

Leaderboard
-----------
{top10_by_score}
