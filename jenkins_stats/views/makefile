# -*- makefile -*-
# ---------------------------------------------------------------------------
# Intent: Retrieve view information for VOLTHA (contributing jobs).
# ---------------------------------------------------------------------------

voltha-views += ci-management
voltha-views += Community-PODs
voltha-views += VOLTHA-2.8
voltha-views += VOLTHA-2.X-Tests
voltha-views += voltha-scale-measurements
voltha-views += voltha-soak
# voltha-views += VOLTHA 2.x verify

deps  := $(foreach view,$(voltha-views),xml/$(view))

##-------------------##
##---]  TARGETS  [---##
##-------------------##
all: voltha-views-get

voltha-views-get: $(deps) voltha-with-space

voltha-views-release: voltha-views-get
	date >> $@.log

voltha-with-space:
	./get_view.sh --view hardcoded-1 # VOLTHA 2.x verify


## -----------------------------------------------------------------------
## Retrieve config data
## -----------------------------------------------------------------------
$(deps):
	./get_view.sh --view $(notdir $@).xml

sterile:
	$(RM) -r json xml

clean:
	$(RM) *.tmp

help:
	@echo "USAGE: $(MAKE)"
	@echo "  voltha-views-get      Retrieve jenkins view definitions"
	@echo "  voltha-views-release  Retrieve jenkins view definitions"
	@echo "  voltha-with-space     Retrieve problematic view names"
	@echo
	@echo "[UTILITY]"
	@echo "    clean           Remove intermediate content and temp files"
	@echo "    sterile         Revert sandbox to a pristine checkout state"
	@echo
	@echo "[VIEWS] - retrieve a jenkins view config.xml by name"
	@echo "  xml/voltha-soak"

# [EOF]
