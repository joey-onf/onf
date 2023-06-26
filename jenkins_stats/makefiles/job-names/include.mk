# -*- makefile -*-

## EXISTS: gather all available jobs or only intact ones ?
##   o convenience macro that allows local stats generation
##   o while retrieving logs from a jenkins server.

job-dir := $(null)
ifndef EXISTS
  include $(MAKEDIR)/job-names/all.mk
else
  include $(MAKEDIR)/job-names/exists.mk
endif

# [EOF]
