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

job-dir := $(null)
job-dir += /home/joey/projects/sandbox/onf/logs
# job-dir += /home/joey/projects/sandbox/onf/logs/var/lib/jenkins/jobs/bbsim_scale_test
# jargs += --jenkins-dir /home/joey/projects/sandbox/onf/logs
jargs += $(addprefix --jenkins-dir$(space),$(job-dir))

jargs += --no-show

# 4 jobs when enabled
# jargs += --view voltha-soak
# jargs += --view voltha-scale-measurements

# 1 job when enabled
# jargs += --job-name bbsim_scale_test



# jargs += --spreadsheet 'jobs.xlsx'
# if $(finstring spreadsheet MAKEDCMDGOALS)
jargs-spread += --spreadsheet 'jobs.xlsx'
# jargs += --view-name 'bbsim_scale_test'

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
	$(RM) *.xlsx
	./jenkins_stats.py $(jargs) $(jargs-spread) 2>&1 | tee log
	 soffice *.xlsx &

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
test-args += -m unittest
check test:
	$(PYTHON) $(test-args) discover -v

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

