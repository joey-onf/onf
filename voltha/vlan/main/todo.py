# -*- python -*-
## -----------------------------------------------------------------------
## Intent: artifact --tags future enhancement list.
## -----------------------------------------------------------------------

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import __main__
import os

from vlan.main        import utils           as main_utils

## -----------------------------------------------------------------------
## Intent: Display pending enhancements for artifact.py --components
## -----------------------------------------------------------------------
def show_todo():
    cmd = os.path.basename(__main__.__file__)
    iam = main_utils.iam()

    print("")
    print("[TODO]")
    print("  %s --todo" % cmd)

    print("""
[TODO: %s]
""" % iam)

    return

# EOF
