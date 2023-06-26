# -*- python -*-
## -----------------------------------------------------------------------
## Intent:
## -----------------------------------------------------------------------

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import __main__
import os

from validate.main         import utils    as main_utils

## -----------------------------------------------------------------------
## Intent: Display pending program enhancements.
## -----------------------------------------------------------------------
def show_todo():
    cmd = os.path.basename(__main__.__file__)
    iam = main_utils.iam()

    print('Usage: %s [options]' % cmd)
    print('''
[TODO: %s]
  o Future enhancement 1.
  o Future enhancement 2.
  o Future enhancement 3.
  o Future enhancement 4.
''' % cmd)

    main_utils.todo()

    return

# EOF
