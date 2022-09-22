# -*- python -*-

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import sys
import argparse

from vlan.main    import todo     as main_todo


## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
class opt_todo_action(argparse.Action):
    """Display program enhancement list."""

    def __call__(self, parser, args, values, option_string=None):
        main_todo.show_todo()

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def add_arg_todo(parser):
    """Register parser switch --todo with an immediate display action."""

    parser.add_argument\
        (
            '--todo',
            action  = opt_todo_action,
            default = False,
            help    = 'Display future enhancement list.',
        )

# [EOF]
