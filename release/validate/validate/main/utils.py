# -*- python -*-
## -----------------------------------------------------------------------
## Intent: This module contains general helper methods
## -----------------------------------------------------------------------

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import sys
import pprint

## ---------------------------------------------------------------------------
## ---------------------------------------------------------------------------
def iam(frame=None):
    """Return name of a called method."""

    if frame is None:
        frame = 1

    func_name = sys._getframe(frame).f_code.co_name # pylint: disable=protected-access
    iam       = "%s::%s" % (__name__, func_name)
    return iam

## ---------------------------------------------------------------------------
## ---------------------------------------------------------------------------
def banner(label, *args, pre=None, post=None) -> None:
    """Format output with delimiters for visibility.

    :param pre: Display leading whitespace.
    :type  pre: bool

    :param post: Display leading whitespace.
    :type  post: bool
    """

    if pre:
        print('')

    hyphens = '-' * 71
    print(" ** %s" % hyphens)
    print(" ** %s" % label)

    for arg in args:
        if isinstance(arg, dict):
            pprint.pprint(arg)
        elif isinstance(arg, list):
            todo = arg
            # todo = list_utils.flatten(arg)
            for line in todo:
                print(" ** %s" % line)
        else:
            print(" ** %s" % arg)

    print(" ** %s" % hyphens)

    if post:
        print('')

## -----------------------------------------------------------------------
## Intent: Display a message then exit with non-zero status.
##   This method cannot be intercepted by try/except
## -----------------------------------------------------------------------
def error(msg, exit_with=None, fatal=None):
    """Display a message then exit with non-zero status.

    :param msg: Error mesage to display.
    :type  msg: string

    :param exit_with: Shell exit status.
    :type  exit_with: int, optional (default=2)

    :param fatal: When true raise an exception.
    :type  fatal: bool (default=False)

    """

    if exit_with is None:
        exit_with = 2

    if fatal is None:
        fatal = false

    if msg:
        if fatal:
            raise Exception("ERROR: %s" % msg)
        else:
            print("")
            print("ERROR: %s" % msg)

    sys.exit(exit_with)

## -----------------------------------------------------------------------
## Intent: Helper method, format an error string then thrown an exception.
##   multi-line strings thrown within an exception are ugly, lines become
##   interspersed with callstack.  Display error text with log delimiters
##   then throw a simple summary message
## -----------------------------------------------------------------------
##  Given:
##    string  - summary to throw exception on
##    array   - strings to display before error is thrown
## -----------------------------------------------------------------------
## Usage:
##        msg = "Detected upload failure"
##        detail = pprint.pformat({
##            'iam' : main_utils.iam(),
##            'ERROR'     : msg,
##            'EXCEPTION' : err,
##            'method-args' : {
##                'src'  : src,
##                'argv' : argv,
##                'tag'  : tag,
##            },
##        }, indent=4)
##        main_utils.my_except(msg, detail)
## -----------------------------------------------------------------------
def my_except(summary, *args):

    me = iam() # iam = iam() reports use before definition in this module
    msg = "ERROR: %s" % summary
    pp = pprint.PrettyPrinter(indent=4, compact=False)

    detail = pp.pformat({
        'iam'     : iam(),
        'args'    : args,
    })

    print("""
===========================================================================
 ** %s
 ** %s
===========================================================================
""" % (msg, detail))

    raise Exception(summary)

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def todo():
    '''Display module future enhancement list.'''

    print('''
[TODO: %s]
  o Future module enhancement 1.
  o Future module enhancement 2.
  o Future module enhancement 3.
''' % iam())

    return

# EOF
