#!/usr/bin/env python
"""Simple script to digest command line args."""

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pdb
import pprint
import sys
import platform

from pathlib import Path

from vlan.main          import utils           as main_utils
from vlan.main          import argparse        as main_getopt
from vlan.main          import help            as main_help

from vlan.workflow      import Utils           as wu_mod

import vlan.network.VlanUtils                  as vu

## FIX THIS: On-demand loading (import loader => A, B, C)
from vlan.workflow     import A               as workspace_A

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def init(debug=None):
    """Script initialization, verify interpreter version is sane."""

    if debug is None:
        debug = False

#    with main_utils.pushd(new_dir=storage):
#        for name in ['foo', 'bar', 'tans']:
#            Path(name).touch()

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def digest_args():
    """Perform actions based on command line args.

    :param argv: Command line args processed by python getopts
    :type  argv: dict

    :return: Success/failure set by action performed
    :rtype : bool
    """

    argv = main_getopt.get_argv()

    args     = ['cidr', 'comment', 'device', 'workflow']
    sizes    = {key:len(argv[key]) for key in args}
    max_size = max([sizes[name] for name in args])

    # ----------------------------
    # Extend arglist with defaults
    # ----------------------------
    if sizes['cidr'] != max_size:
        pprint.pprint({
            'error' : 'Detected excess command line arguments',
            'max'   : max_size,
            'args'  : args,
            'sizes' : sizes,
        })

    for idx in range(sizes['comment'], max_size):
        argv['comment'] += ['Space for rent']

    for idx in range(sizes['device'], max_size):
        argv['device'] += [ argv['device'][-1] ]

    for idx in range(sizes['workflow'], max_size):
        argv['workflow'] += [ argv['workflow'][-1] ]

    for idx in range(0, len(argv['cidr'])):

        device = argv['device'][idx]
        cidr   = argv['cidr'][idx]
        # comment = argv['comment'][idx]
        foo=\
            {
                'comment' : argv['comment'][idx]
            }

        ## TODO: Dynamic objects based on --workflow XYZ
        obj = workspace_A.A(device, cidr, foo)
        conf = obj.gen_conf()
        print(''.join(conf))

    return

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def main(argv_raw):
    """Off to the races."""

    iam = main_utils.iam()
    debug = False
    if debug:
        print(" ** %s: BEGIN" % iam)

    init()
    main_getopt.getopts(argv_raw)
    digest_args()
    sys.exit(0)

##----------------##
##---]  MAIN  [---##
##----------------##
if __name__ == "__main__":
    main(sys.argv[1:]) # NOSONAR

# [EOF]
