#!/bin/bash
## -----------------------------------------------------------------------
## Intent: Post git commit, rebase to merge dev branch with latest changes
##         on remote master branch.
## -----------------------------------------------------------------------
## 0) Backup local sandbox
## 1) git clone       (git clone ...)
## 2) create branch   (git checkout -b dev-tux)
## 3) Edit away
## 4) Commit changes  (git ci --message "doing something")
## 5) Rebase
##     - infer dev branch name
##     - checkout master
##     - update local master branch to match remote:master
##     - checkout dev branch
##     - merge
## -----------------------------------------------------------------------
## Setup:
##   % git clone repo
##   % cd repo
##   % git create -b dev-{user}
##   % vi *.sh
##   % git add ....
##   % git commit --mesage "did something"
##   % rebase.sh
##   % git review
## -----------------------------------------------------------------------

my_branch="$(git rev-parse --abbrev-ref HEAD)"

case "$my_branch" in
    dev-${USER}) ;;
    review/*_*/*) ;;

    *)
	echo "ERROR: Unknown branch"
	declare -p my_branch
	exit 1
	;;
esac


## Check sandbox name and disable sterile when needed
# make sterile

##------------------##
##---]  MASTER  [---##
##------------------##
echo "** BACKUP: ENTER"
time tar czvf ../rebase.backup.tgz .
echo "** BACKUP: LEAVE"

git checkout master
git pull --ff-only origin master

git checkout "${my_branch}"
git rebase -i master

git diff --name-only master 2>&1 | less

echo "[TODO]: git review [--reviewers]"

# [EOF]
