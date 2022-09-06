# -*- python -*-
""" . """

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pprint
import ipaddress

from vlan.main   import utils as main_utils

class DhcpUtils:
    """ . """

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, args=None):
        """Constructor.

        :param args: 
        :type  args: dict, optional
        """
        
        if args is None:
            args = {}

        for key,val in args.items():
            setattr(self, key, val)

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def gen(self, cidr) -> str:

        #subnet 10.11.1.0 netmask 255.255.255.0 {
        # range 10.11.1.1 10.11.1.100;   # Enable full range, not limited to 100
        # option routers 10.11.1.254;
        # option domain-name-servers 8.8.8.8 ;
        # }
        return
}

        
        
# [EOF]
