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
import pdb

import argparse
import pprint

from IPy import IP  # IPv4 & IPv6
from iptools     import ipv4, ipv6
import ipaddress

from vlan.main   import argparse_todo

from vlan.main   import utils as main_utils
from vlan.main   import argparse_actions

import vlan.network.VlanUtils as vu

## -----------------------------------------------------------------------
## Intent: Validate --netmask xx.xx.xx/ddd value passed
## -----------------------------------------------------------------------
def valid_vlan_arg(cidr: str) -> str:
    """ . """

    obj = vu.VlanUtils()
    if not obj.is_valid(cidr):
        msg = "\n%s" % obj.error
        raise argparse.ArgumentTypeError(msg)

    return cidr

## -----------------------------------------------------------------------
## Intent:
## -----------------------------------------------------------------------
def NYI(arg:str) -> str:
    """ . """

    if True:
        raise argparse.ArgumentTypeError("Not yet implemented")
    return(arg)

## -----------------------------------------------------------------------
## Intent: Validate --netmask xx.xx.xx/ddd value passed
## -----------------------------------------------------------------------
## https://medium.com/@zackbunch/how-to-create-custom-argparse-types-in-python-608c17d1f94a
## -----------------------------------------------------------------------
def valid_netmask_ipaddress(netmask: str) -> str:
    """Custom argparse type for netmask string validation of command line args."""

    import pdb
    pdb.set_trace()
    x = ipaddress.ip_network(netmask)

    ans = False
    if ipaddress.ip_network(netmask):
        ans = True
    else:
        err = "%s is invalid" % netmask
        raise argparse.ArgumentTypeError(err)

    return netmask

        
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
                 prog = 'foobar.py',
                 description = 'Simple argparse module calls'
             )

    ## -----------------------------------------------------------------------
    ##
    ## -----------------------------------------------------------------------
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    ## -----------------------------------------------------------------------
    ## Deployment args
    ## -----------------------------------------------------------------------
    parser.add_argument('--backup',
                        # action  = 'store_true',
                        # default = False,
                        action  = 'store',
                        type    = NYI,
                        help    = 'Archive network configs in this directory',
                    )

    parser.add_argument('--dhcp',
                        # action  = 'store_true',
                        # default = False,
                        action  = 'store',
                        type    = NYI,
                        help    = 'Generate DHCP rules for the BGP',
                    )

    parser.add_argument('--comment',
                        action  = 'append',
                        default = [],
                        help    = 'ACT/FIN comments for config files',
                    )

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    
    ## -----------------------------------------------------------------------
    ## Device to configure: reset --vlan* values
    ## -----------------------------------------------------------------------
    parser.add_argument('--cidr',
                        action   = 'append',
                        default  = [],
                        required = True,
                        type     = valid_vlan_arg,
                        help     = 'VLAN netmask, used to derive vlan configuration.',
                    )
    parser.add_argument('--device',
                        action   = 'append',
                        required = True,
                        default  = [],
                        help     = 'Network device to configure',
                    )
     
    parser.add_argument('--workflow',
                        action   = 'append',
                        required = True,
                        help     = 'Workflow template specifying vlan configuration',
                    )

    ## -----------------------------------------------------------------------
    ## Option by constant selection list
    ## -----------------------------------------------------------------------
    parser.add_argument('--prefix',
                        action  = 'store',
                        type     = NYI,
                        help    = 'Label prefix used to name config files',
                    )

    ## -----------------------------------------------------------------------
    ## Program modes
    ## -----------------------------------------------------------------------
    parser.add_argument('--debug',
                        action  = 'store_true',
                        default = False,
                        help    = 'Enable debug mode',
                    )

    parser.add_argument('--dry-run',
                        action  = 'store_true',
                        default = False,
                        help    = 'Read-only mode, display switch actions',
                    )

    argparse_todo.add_arg_todo(parser)
#    parser.add_argument('--todo',
#                        # action  = 'argparse_actions.opt_todo_action',
 #                       action  = 'opt_todo_action',
 #                       help    = 'Display future enhancement list.',
 #                   )

    parser.add_argument('--verbose',
                        action  = 'store_true',
                        default = False,
                        help    = 'Enable verbose mode',
                    )

    namespace = parser.parse_args()
    return

# [SEE ALSO]
# -----------------------------------------------------------------------
# [ARGPARS]
#   o https://docs.python.org/3/library/argparse.html
# Read args from a response file:
#   o https://stackoverflow.com/questions/27433316/how-to-get-argparse-to-read-arguments-from-a-file-with-an-option-rather-than-pre
# 
#   o https://medium.com/@zackbunch/how-to-create-custom-argparse-types-in-python-608c17d1f94a
# 
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# https://developers.redhat.com/blog/2018/10/22/introduction-to-linux-interfaces-for-virtual-networking
# 
# https://www.computernetworkingnotes.com/ccna-study-guide/vlan-configuration-commands-step-by-step-explained.html
# -----------------------------------------------------------------------

# [EOF]
                 
