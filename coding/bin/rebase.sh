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

if git remote -v show 2>&1 | grep -q 'github'; then
    echo "ERROR: Detected a github repo, outa here"
    exit 1
fi

my_branch="$(git rev-parse --abbrev-ref HEAD)"

case "$my_branch" in
    dev-${USER}*) ;;
    review/*_*/*) ;;
    voltha-2.12) ;;
    voltha-2.11) ;;
    voltha-2.10) ;;

    voltha-2.12) declare -g -i release_branch=1 ;;

    *)
        echo "ERROR: Unknown branch"
        declare -p my_branch
        exit 1
        ;;
esac

# [TODO] Interrogate git branch -vv to find origin
# [TODO] Value needed for rebase -i

# % git branch -vv
# -----------------------------------------------------------------------
# * dev-joey 253fa01b [origin/voltha-2.12: ahead 1] repo:voltha-go Post tag & branch activity
#   master   4e0e0347 [origin/master] [VOL-5247] repo:voltha-go release patching prep
# -----------------------------------------------------------------------

# https://gerrit.opencord.org/c/voltha-go/+/35016

##------------------##
##---]  MASTER  [---##
##------------------##
if [ "$USER" == 'joey' ]; then
    make sterile
fi

echo "** BACKUP: ENTER"
time tar czvf ../rebase.backup.tgz .
echo "** BACKUP: LEAVE"

git checkout master
git pull --ff-only origin master
# git pull --ff-only origin master

git checkout "${my_branch}"
git rebase -i master

git diff --name-only master 2>&1 | less

echo "[TODO]: git review [--reviewers]"

# [EOF]
