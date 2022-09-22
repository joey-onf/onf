# -*- python -*-
"""Script command line argument parsing.

..todo: https://docs.python.org/3/library/argparse.html##
"""

##-------------------##
##---]  GLOBALS  [---##
##-------------------##
ARGV      = None
namespace = None

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
from pathlib import Path

import pdb

import argparse
import pprint

from IPy import IP  # IPv4 & IPv6
from iptools     import ipv4, ipv6
import ipaddress

from vlan.main   import argparse_todo

from vlan.main   import utils as main_utils
from vlan.main   import argparse_actions

## -----------------------------------------------------------------------
## Intent: Validate --netmask xx.xx.xx/ddd value passed
## -----------------------------------------------------------------------
def valid_directory(path: str) -> str:
    """Validate argument is a filesystem directory"""

    iam = main_utils.iam()
    if not Path(path).is_dir():
        err = "%s: A valid directory is required %s" % (iam, path)
        raise argparse.ArgumentTypeError(path)

    return path

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def get_argv():
    """Retrieve parsed command line switches.

    :return: Parsed command line argument storage
    :rtype : dict
    """

    global ARGV
    global namespace

    if ARGV is None:
        # Normalize argspace/namespace into a getopt/dictionary
        # Program wide syntax edits needed: args['foo'] => args.foo
        arg_dict = {}
        for arg in vars(namespace):
            arg_dict[arg] = getattr(namespace, arg)
        ARGV = arg_dict

    return ARGV

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def set_argv(args:dict) -> None:
    '''Unit test helper'''

    global ARGV
    ARGV = args

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def getopts(argv, debug=None) -> None:
    """Parse command line args, check options and pack into a hashmap

    :param argv: values passed on the command line
    :param debug: optional flag to enable debug mode

    :return: Digested command line arguments
    :rtype : dict

    :raises  ValueError

    ..note: A dictionary is returned for backward compatibility.
    ..note: arg syntax should change from foo['debug'] to foo.debug
    ..note: allowing raw library return type(namespace) to be used.

    ..todo: support --dry-run, deploy actions w/o final import request.

    ..todo: Strange decorate a switch with required=True.  Pass switch through
    ..todo: --response fails even though value(s) are in parsed args namespace.

    .. versionadded:: 1.2
    """

    global ARGV
    global namespace

    iam = main_utils.iam()

    if debug is None:
        debug = False

    if debug:
        pprint.PrettyPrinter(indent=4).pprint({
            'iam'   : iam,
            'argv'  : argv,
            'event' : 'BEGIN',
        })

    parser = argparse.ArgumentParser\
             (
                 # prog = 'foobar.py',
                 description = 'Traige statistics from jenkins jobs',
             )

    ## -----------------------------------------------------------------------
    ## Program modes
    ## -----------------------------------------------------------------------
    parser.add_argument('--debug',
                        action  = 'store_true',
                        default = False,
                        help    = 'Enable debug mode',
                    )

    argparse_todo.add_arg_todo(parser)

    parser.add_argument('--verbose',
                        action  = 'store_true',
                        default = False,
                        help    = 'Enable verbose mode',
                    )

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    parser.add_argument('--jenkins-dir',
                        action  = 'store',
                        type    = valid_directory,
                        help    = 'Path to a jenkins job directory',
                    )
    
    parser.add_argument('--job-name',
                        action  = 'append',
                        default = [],
                        help    = 'Jenkins job name to generate stats for',
                    )

    parser.add_argument('--view-name',
                        action  = 'append',
                        default = [],
                        help    = 'Jenkins UI job view to generate stats for',
                    )

    ## -----------------------------------------------------------------------
    ## Reporting
    ## -----------------------------------------------------------------------    
    parser.add_argument('--show',
                        action  = 'store_true',
                        default = True,
                        help    = '[REPORT] Render to screen'
                    )
    parser.add_argument('--no-show',
                        action  = 'store_false',
                        dest    = 'show',
                        help    = '[REPORT] Render to screen'
                    )

    parser.add_argument('--spreadsheet',
                        action  = 'store',
                        help    = '[REPORT] Render as a spreadsheet'
                    )
    
    
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    namespace = parser.parse_args()
    return

# [SEE ALSO]
# [EOF]
                 
