#!/bin/bash

cat <<EOF
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
Clone a sandbox, create a developer branch, rebase,

1) git clone                          # clone a sandbox
2) git checkout -b dev-${USER}        # create a developer branch
3) hack                               # modify to taste

4) git ci --message "release the hounds"

5) git checkout master                # checkout master branch
6) git pull --ff-only origin master   # retrieve latest remote

7) git checkout dev-${USER}           # back to my branch
8) git rebase -i master               # merge with master

9) git review --reviewers foo@opennetworking.org bar@opennetworking.org
                                      # create a pull request

Augment an existing pull request
================================

Locate pull request Commit-ID (not git commit ID) of interest
  o https://gerrit.opencord.org
    - If ID hash is known use the search box.
      - search: I0a3425dc1b036a43a7155bb284d17898baef46f3
      - search: 33179
    - else visit gerrit and review outstanding pull requests:
    - Commit-IDs can be found appended to your checkin message.
  o https://gerrit.opencord.org/c/voltha-docs/+/33179
    - Helpful to record commit-IDs or pull request URL in wiki as a clickable link.0
    - Captured from stdout after running 'git review'

  o Once you have the changeset ID


Checkout your sandbox if not already on disk:
  o run one of
    - git review -d I0a3425dc1b036a43a7155bb284d17898baef46f3
    - git review -d 33179

[NOTE] - your sandbox will contain one of two distinct branches:
  o git branches            # show available
  o git checkout review/[submitter]/[branch]
                            # a clean checkout will always create this branch

Modify sources then commit
  o git commit --amend      # --amend is important!  Do not use git commit here
  # https://stackoverflow.com/questions/12487791/how-to-amend-review-issues-in-gerrit-when-there-is-a-second-newer-review-also

Merge with master branch for pending pull request
  o git rebase -i master
    - changesets will appear as 'pick'
    - When multiple changesets are listed
      - modify the initial changeset to be 'edit'
  o git commit --amend
  o git rebase --continue
  o git review





https://stackoverflow.com/questions/53209237/how-to-solve-merge-conflict-in-a-approved-review-in-gerrit


[INSTALL COMMIT HOOK]
# https://gerrit-review.googlesource.com/Documentation/intro-gerrit-walkthrough.html

# curl -Lo .git/hooks/commit-msg http://review.example.com/tools/hooks/commit-msg
# scp -p -P 29418 gerrit.opencord.org:hooks/commit-msg ci-management/.git/hooks/
# chmod +x ci-management/.git/hooks/commit-msg
# git push origin HEAD:refs/for/<branch_name>


## See also: https://wiki.onosproject.org/display/ONOS/Sample+Gerrit+Workflow

https://wiki.onosproject.org/display/ONOS/Sample+Gerrit+Workflow


EOF


