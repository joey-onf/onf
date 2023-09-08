# -*- makefile -*-
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

.DEFAULT_GOAL := args

TOP         ?= .
include $(TOP)/config.mk
include $(TOP)/makefiles/include.mk

PYTHON      ?= $(HOME)/.venv/3.10.6/bin/python 

main        := bin/validate.py

##-------------------##
##---]  TARGETS  [---##
##-------------------##

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
all: args

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
main-args := $(null)

main-args += --debug
main-args += --trace
main-args += --verbose

main-args += --voltha-2.11
main-args += --my-host foo.bar.org
main-args += --my-list itemA
main-args += --my-list itemB
main-args += --my-scalar 5

args:
	$(main) $(main-args)

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
edit:
	./edit.sh

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
invalid:
	@echo
	-$(main) --my-host area-51

	@echo
	-$(main) --my-host 'croak'

	@echo
	-$(main) --my-host '1.2.3.4'

# -----------------------------------------------------------------------
## -----------------------------------------------------------------------
main-help:
	$(main) --help

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
.PHONY: todo
todo ::
	$(main) --$@ stub-required-arg

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
version:
	$(main) --$@

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
clean ::
	-$(HOME)/etc/cleanup

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
help ::
	@echo "USAGE: $(MAKE)"
	@echo "  all        Invoke $(main)"
	@echo "  args       Invoke script with a variety of args"
	@echo "  todo       Display enhancement list"
	@echo "  version    Display script version"
	@echo
	@echo "[ERROR]"
	@echo "  invalid    An example of passing invalid arguments"
	@echo
	@echo "[MISC]"
	@echo "  edit       Load sources into an editor"
	@echo
	@echo "[HELP]"
	@echo "  help       Display makefile targets"
	@echo "  main-help  Display program usage"
	@echo
	@echo "[EOF]"

# submodules:
#	git submodule add https://github.com/opencord/onf-make.git
#	ssh://joey@opennetworking.org@gerrit.opencord.org:29418/onf-make
# [EOF]
