#!/bin/bash -x

# Push the updated entries.csv and README.md file to GitHub
if [ -n "$GITHUB_API_KEY" ]; then
  cd $TRAVIS_BUILD_DIR
  # This is because Travis clones things in a bullshit detached state and shit gets
  # all Rick and Morty like if you try and hack it into force pushing back to GitHub
  # Got a better fix? PLEASE OPEN A PR
  git clone git@github.com:$TRAVIS_REPO_SLUG.git tmp
  cp entries.csv tmp/
  cp README.md tmp/
  cd tmp/
  git add entries.csv
  git add README.md
  git -c user.name="referee" -c user.email="referee" commit -m "Updating scoreboard [ci skip]"
  git push -q -f https://$GITHUB_USER:$GITHUB_API_KEY@github.com/goto-obs/goto-vegas master
fi
