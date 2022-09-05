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

# from vlan.workspace     import loader => A, B, C
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
def workflow_A(argv):
    """Perform actions based on command line args.

    :param argv: Command line args processed by python getopts
    :type  argv: dict

    :return: Success/failure set by action performed
    :rtype : bool
    """

    argv = main_getopt.get_argv()

    if not argv['device']:
        raise Exception('--device= is required')
    device = argv['device'][0]

    obj = vu.VlanUtils()
    ans = True
    for cidr in argv['cidr']:
        for line in [
                #
                '#',

                # ip link add link ${device} name ${device}.11 type vlan id 11
                obj.fmt_add_vlan_by_id(device, cidr),

                # ip link set ${device} up
                obj.fmt_vlan_device_up(device, cidr),

                # ip link add link ${device}.11 name ${device}.11.111 type vlan id 111
                obj.fmt_add_vlan2_by_id(device, cidr),

                # ip link set ${device}.11.111 up 
                obj.fmt_vlan2_device_up(device, cidr),

                # ip addr add 10.11.111.254/24 dev ${device}.11.111
                obj.fmt_add_netmask_by_vlan2(device, cidr),
        ]:
            print(line)

    return ans

## -----------------------------------------------------------------------
##
## -----------------------------------------------------------------------
def workflow_C(argv):

    argv = main_getopt.get_argv()

    if not argv['device']:
        raise Exception('--device= is required')

    obj = vu.VlanUtils()

    ans = True
    for cidr in argv['cidr']:
        fields   = obj.cidr_split(cidr)
        octets   = fields['octets']
        device   = argv['device'][0]
        vlan_id  = octets[1]
        device_X = "%s.%s" % (device, vlan_id)

        workflow.Utils

        
        for line in [
                #
                '#',
# ip link add link ${device} name ${device}.54 type vlan id 54
                obj.fmt_B(device, device_X, vlan_id),

# ip link set ${device}.54 up
                obj.link_up_B(device_X),
        ]:
            print(line)

    return ans

## -----------------------------------------------------------------------
## DT-PON17.conf
## -----------------------------------------------------------------------
def workflow_B(argv):

    cidr   = argv['cidr'][0]
    device = argv['device'][0]

    args = argv['comment'][0]
    conf = workspace_A.A(device, cidr, args)
    print(''.join(conf))

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

        # conf = workflow_B(device, cidr, argv)
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

    # cleanup
    sys.exit(0)

##----------------##
##---]  MAIN  [---##
##----------------##
if __name__ == "__main__":

    main(sys.argv[1:]) # NOSONAR

# [EOF]
