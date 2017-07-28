#!/bin/bash -x

# Push the updated entries.csv and README.md file to GitHub
if [ -n "$GITHUB_API_KEY" ]; then
  cd $TRAVIS_BUILD_DIR
  #git checkout -b master
  git reset --hard $TRAVIS_COMMIT
  git add entries.csv README.md
  git -c user.name="referee" -c user.email="referee" commit -m "Updating scoreboard [ci skip]"
  git push -q -f https://$GITHUB_USER:$GITHUB_API_KEY@github.com/goto-obs/goto-vegas master
fi
