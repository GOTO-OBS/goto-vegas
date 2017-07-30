#!/bin/bash -x

# Push the updated entries.csv and README.md file to GitHub
if [ -n "$GITHUB_API_KEY" ]; then
  cd $TRAVIS_BUILD_DIR
  cp entries.csv tmp/
  cp README.md tmp/
  cd tmp/
  git add entries.csv
  git add README.md
  git -c user.name="referee" -c user.email="referee" commit -m "Updating scoreboard [ci skip]"
  git push -q -f https://$GITHUB_USER:$GITHUB_API_KEY@github.com/goto-obs/goto-vegas master
fi
