#!/usr/bin/env bash
#
# assumes you're on develop branch with a clean git index
#

# reset to develop branch
# hub-reset-topic-branch

git checkout master
git merge develop
git push origin master

# todo: string formatting with args
git tag -a -m "bumps version to 0.{}.{}" 0.x.x
git push origin --tags


# now ready to build and deploy the release..
./release.sh
