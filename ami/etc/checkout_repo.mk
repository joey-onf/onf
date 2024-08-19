# -*- makefile -*-
## -----------------------------------------------------------------------
## Intent: Anonymous checkout repositor(y|ies) for local build
## -----------------------------------------------------------------------

GIT ?= /usr/bin/env git

repos := $(null)
repos += voltha-protos

all : $(repos)

$(repos) :

	@printf '\nClone: %s\n' "$@"
	@$(GIT) clone "https://gerrit.opencord.org/$@"

	@printf '\nReConfigure git to prevent commits from prototype sandbox\n'
	@cd $@ && git remote set-url --push origin no_push
	@cd $@ && git config user.email 'foo@bar.com'
	@cd $@ && git config user.name 'Jenkins Server'

clean ::

sterile :: clean
	$(RM) -r $(repos)

# [EOF]
