# -*- makefile -*-

GIT ?= /usr/bin/env git

repos := $(null)
repos += voltha-protos

all : $(repos)

$(repos) :
        $(GIT) clone "https://gerrit.opencord.org/$@"
        cd $@ && git remote set-url --push origin no_push
        git config user.email 'foo@bar.com'
        git config user.name 'Jenkins Server'

clean ::

sterile :: clean
        $(RM) -r $(repos)

# [EOF]
