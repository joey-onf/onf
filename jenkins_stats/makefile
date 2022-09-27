# -*- makefile -*-
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

null 	:=#
space	:=$(null) $(null)

# -----------------------------------------------------------------------
# PYTHON ?= python
# kubuntu: why are you failing when CMD is available $PATH ?
# rebuild GNU make from source to determine if this is a security enhancement (?)
# -----------------------------------------------------------------------
PYTHON  ?= /home/joey/.venv/3.10.6/bin/python 

jargs        := $(null)

job-dir-opts += /var/lib/jenkins/jobs
job-dir-opts += /home/joey/projects/sandbox/onf/logs
job-dir      := $(firstword $(wildcard $(job-dir-opts)))
jargs        += $(addprefix --jenkins-dir$(space),$(job-dir))

jargs        += --no-show # squelch stdout

# 4 jobs when enabled
# jargs += --view voltha-soak
# jargs += --view voltha-scale-measurements
# jargs += --view XOS-Integration-Tests

# Report on a single job
# jargs += --job-name bbsim_scale_test



# jargs += --spreadsheet 'jobs.xlsx'
# if $(finstring spreadsheet MAKEDCMDGOALS)
jargs-spread += --spreadsheet 'jobs.xlsx'
# jargs += --view-name 'bbsim_scale_test'

# ---------------------------
# Conditional interactive use
# ---------------------------
soffice-cmd := $(shell which soffice 2>/dev/null)
SOFFICE = $(if $(soffice-cmd),$(soffice-cmd),@#)
# SOFFICE := $(null)\#

##-------------------##
##---]  TARGETS  [---##
##-------------------##
all: spreadsheet

view:
	./jenkins_stats.py $(jargs) 2>&1 | tee log

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
views:
	$(MAKE) -C views voltha-views-release

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
spreadsheet:
	-@pkill soffice
	$(RM) *.xlsx
	./jenkins_stats.py $(jargs) $(jargs-spread) 2>&1 | tee log
	 $(SOFFICE) *.xlsx &

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
test-args += -m unittest
check test:
	$(PYTHON) $(test-args) discover -v

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
venv := $(HOME)/.venv/3.6.8
install:
	python3 -m $(venv)	
	source $(venv)/bin/activate && pip install IPy
	source $(venv)/bin/activate && pip install iptools
	source $(venv)/bin/activate && pip install openpyx

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
clean:
	-$(HOME)/etc/cleanup
	$(RM) *.xlsx

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
help:
	@echo "USAGE: $(MAKE)"
	@echo "  all      Generate summary job stats for (jenkins 'opencord.org')"
	@echo "  test     Invoke available unit tests (find . -name 'test_*.py')"
	@echo "  views    Retrieve jenkins view data for reporting."
#	@echo "  [check|smoke]    Invoke quick unit tests (max_runtime=30-sec')"
	@echo ''
	@echo "[HELPER]"
	@echo "  clean    

# [EOF]
