# -*- makefile -*-
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

all :

init ::
	etc/setup.sh

install : init
	./install.sh

clean ::
	find . \( -name '*~' -o -name '#*#' -o -name '\.#*' \) -print0 \
	  | xargs --null --no-run-if-empty $(RM)

# [EOF]
