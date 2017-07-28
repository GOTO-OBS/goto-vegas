#!/bin/bash -x

# Push the updated entries.csv and README.md file to GitHub
if [ -n "$GITHUB_API_KEY" ]; then
  cd $TRAVIS_BUILD_DIR
  git add entries.csv README.md
  git -c user.name="referee" -c user.email="referee" commit -m "Updating scoreboard"
  git push -q -f https://$GITHUB_USER:$GITHUB_API_KEY@github.com/$TRAVIS_REPO_SLUG master
fi