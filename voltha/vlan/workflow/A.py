# -*- python -*-
""" . """

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pdb
import pprint
import ipaddress

import re

from vlan.main   import utils as main_utils

import vlan.network.VlanUtils                  as vu_mod
from vlan.workflow      import Utils           as wu_mod


class A:
    """This module is used to generate workspace A vlan configs."""

    comment = None
    device  = None
    cidr = None

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, device, cidr, args=None):
        """Constructor.
        :param args: 
        """

        if args is None:
            args = {}

        self.device = device
        self.cidr   = cidr

        if 'comment' in args:
            self.comment = args['comment']
            
        for key,val in args.items():
            setattr(self, key, val)
    
    ## -----------------------------------------------------------------------
    ## DT-PON17.conf
    ## -----------------------------------------------------------------------
    def gen_conf(self) -> list:
        """Generate a workflow A config given parameters.

        :return: Workflow A config values.
        :rtype : list
        """

        device = self.device
        cidr = self.cidr

        fields = vu_mod.VlanUtils().cidr_split(cidr)
        octets = fields['octets']

        vlan_xx = octets[1]
        vlan_yy = octets[2]
        vlan_xy = '.'.join(octets[1:3])

        device_X = "%s.%s" % (device, vlan_xx)

        values=\
            {
                # cidr: '10.11.111.254/24,
                #
                'device'     : device,
                'device_xx'  : "%s.%s" % (device, vlan_xx),
                'device_xy'  : "%s.%s" % (device, vlan_xy), # 11.111
                'device_yy'  : "%s.%s" % (device, vlan_yy),
                #
                'vlan_id_xx' : vlan_xx, # 11
                'vlan_id_yy' : vlan_yy, # 111
                #
                'cidr'       : cidr,
            }

        ans = []
        if not self.comment is None:
            ans += ['# [ACT]: %s\n' % self.comment]

        ans += [ wu_mod.Utils().fill_in('A.tmpl', values) ]

        if not self.comment is None:
            ans += ['# [FIN]: %s\n' % self.comment]

        return ans

# [EOF]
