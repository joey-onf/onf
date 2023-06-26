# -*- python -*-
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import __main__
import os
import sys

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def get_help_switches():
    """Return a list of command line switches resolved by this module.

    ...versionadded: 1.0
    """

    return [
        'help',
        'help-A',
        'help-B',
        'help-C',
        'help-D',
    ]

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def show_usage():
    """Display sample command line usage"""

    cmd = os.path.basename(__main__.__file__)

    print("""
## Verify basic interaction
%% %s --A --B
""" % cmd)

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def show_usage_A():
    """Display command(A) usage"""

    print("""
  --wip
  --changeset cs1[..n]
""")

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def show_usage_B():
    """Display sample command line usage for B."""

    print("""
# Export project files from BAT_Guineapig
  --NOT-YET-IMPLEMENTED
  --foo        # enable foo
  --bar        # enable bar

# git resources
  --NOT-YET-IMPLEMENTED
  --changeset 'b5ff3ec2624911ec881e00505687635e'
""")

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def show_usage_search():
    """Display sample command line usage for search endpoint(s)"""

    print("""
  --NOT-YET-IMPLEMENTED
  --lookup   # prepare arguments for export
  --display  # show results
""")

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def show_help():
    """Display supported command line arguments"""

    print("""
[FOO]
  --A            enable mode A
  --AB           enable mode B

[MODES]
  --debug        Enable debug mode
  --verbose      Enable verbose mode, display additional output and status

[HOWTO]
  --help         Display command line arguments and usage.
""")

## -----------------------------------------------------------------------
## Intent: Display command usage
## -----------------------------------------------------------------------
def usage(err=None, arg=None):
    """Display command arguments and usage

    :param err: Error to display due to invalid arg parsing.
    :type  err: String

    :param arg: --help* command line argument digested by argparse.py
    :type  arg: String

    :raises  ValueError

    ...versionadded: 1.1
    """

    cmd = os.path.basename(__main__.__file__)
    print("USAGE: %s" % cmd)

    show_help()

    if err:
        print("")
        print("ERROR: %s" % err)
        sys.exit(2) # exit with status

    if arg in get_help_switches():
        print("[USAGE]")
        print('=' * 75, end='') # print w/o newline, implicitly added by print-triple-quoted below

        if 'help-a' in arg:
            show_usage_automation()

        elif 'help-d' in arg:
            show_usage_deployment()

        elif 'help-e' in arg:
            show_usage_export()

        elif 'help-s' in arg:
            show_usage_search()

        elif 'help' == arg:
            print('')

        else:
            raise ValueError("Detected invalid --help argument [%s]" % arg)

        print('=' * 75)

    else:
        show_usage()

    sys.exit(os.EX_USAGE)

# EOF
