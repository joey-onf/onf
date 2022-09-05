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

class VlanUtils:
    'Common base class for all employees'

    error  = None
    errors = []

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, args=None):
        """Constructor.
        :param args: 
        """
        if args is None:
            args = {}

        for key,val in args.items():
            setattr(self, key, val)

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __clear__(self):
        setattr(self, 'error', None)

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def cidr_split(self, cidr) -> dict:
        """Split a cidr value into components.

        :param cidr: xxx.xxx.xxx.xxx/xxx
        :type  cidr: str
        
        :return: Fields extractd from cidr string.
        :rtype : dict
        """
        
        address,mask = ipaddress\
            ._IPAddressBase\
            ._split_addr_prefix(cidr)

        ans=\
            {
                'octets' : address.split('.'),
                'addr'   : address,
                'mask'   : mask,
            }
        return ans
        
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def fmt_add_vlan_by_id(self, device, name, vlan_id):

        # line = "ip link add link %s name %s.%s type vlan id %s" % (device, vlan)
        line = ' '.join([
            "ip link add link %s" % (device),
            "name %s.%s"          % (name),
            "type vlan id %s"     % (vlan_id),
        ])

        return line

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def fmt_add_vlan_by_id(self, device, cidr):
        fields = self.cidr_split(cidr)

        octets = fields['octets']
        vlan_X  = octets[1]
        vlan_XY = "%s.%s"  % (octets[1], octets[2])
        vlan_sub = "%s.%s" % (device, vlan_XY)

        # line = "ip link add link %s name %s.%s type vlan id %s" % (device, vlan)
        line = ' '.join([
            "ip link add link %s" % (device),
            "name %s.%s"          % (device, octets[1]),
            "type vlan id %s"     % (vlan_X),
        ])

        name = "%s.%s" % (device, octets[1])
        return self.fmt_add_vlan_by_id(device, name, vlan_id)
        # return line

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def fmt_add_vlan_by_id_orig(self, device, cidr):
        fields = self.cidr_split(cidr)

        octets = fields['octets']
        vlan_X  = octets[1]
        vlan_XY = "%s.%s"  % (octets[1], octets[2])
        vlan_sub = "%s.%s" % (device, vlan_XY)

        # line = "ip link add link %s name %s.%s type vlan id %s" % (device, vlan)
        line = ' '.join([
            "ip link add link %s" % (device),
            "name %s.%s"          % (device, octets[1]),
            "type vlan id %s"     % (vlan_X),
        ])

        return line

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def fmt_add_vlan_by_id(self, device, cidr):
        fields = self.cidr_split(cidr)

        octets = fields['octets']
        vlan_X  = octets[1]
        vlan_XY = "%s.%s"  % (octets[1], octets[2])
        vlan_sub = "%s.%s" % (device, vlan_XY)

        # line = "ip link add link %s name %s.%s type vlan id %s" % (device, vlan)
        line = ' '.join([
            "ip link add link %s" % (device),
            "name %s.%s"          % (device, octets[1]),
            "type vlan id %s"     % (vlan_X),
        ])

        name = "%s.%s" % (device, octets[1])
        return self.fmt_add_vlan_by_id(device, name, vlan_id)
        # return line

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def fmt_vlan_device_up(self, device, cidr):
        fields   = self.cidr_split(cidr)
        device_X = "%s.%s" % (device, fields['octets'][1])

        line = 'ip link set %s up' % (device_X)
        return line
  
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def link_up_B(self, device_id):
        line = 'ip link set %s up' % (device_id)
        return line
  
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def fmt_add_vlan2_by_id(self, device, cidr):
        fields = self.cidr_split(cidr)

        octets = fields['octets']
        vlan_X  = "%s.%s"  % (device, octets[1])
        vlan_XY = "%s.%s"  % (vlan_X, octets[2])
        vlan_sub = "%s.%s" % (device, vlan_XY)

        # line = "ip link add link %s name %s.%s type vlan id %s" % (device, vlan)
        line = ' '.join([
            "ip link add link %s" % (vlan_X),
            "name %s"             % (vlan_XY),
            "type vlan id %s"     % octets[2],
        ])

        return line

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def fmt_vlan2_device_up(self, device, cidr):
        fields    = self.cidr_split(cidr)
        octets    = fields['octets']
        device_XY = "%s.%s.%s" % (device, octets[1], octets[2])

        line = 'ip link set %s up' % (device_XY)
        return line

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def fmt_add_netmask_by_vlan2(self, device, cidr):
        fields = self.cidr_split(cidr)

        octets    = fields['octets']
        vlan_X    = "%s.%s"  % (device, octets[1])
        device_XY = "%s.%s"  % (vlan_X, octets[2])

        # ip addr add 10.11.111.254/24 dev ${device}.11.111
        line = ' '.join([
            "ip addr add %s" % (cidr),
            "dev %s"         % (device_XY),
        ])

        return line

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def fmt_B(self, cidr, vlan_id):
        fields = self.cidr_split(cidr)

        octets    = fields['octets']
        vlan_X    = "%s.%s"  % (device, octets[1])
        device_XY = "%s.%s"  % (vlan_X, octets[2])

        # ip addr add 10.11.111.254/24 dev ${device}.11.111
        line = ' '.join([
            "ip addr add %s" % (cidr),
            "dev %s"         % (vlan_id),
        ])

        return line
    
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def is_valid_cidr(self, cidr) -> bool:
        """ . """

        ans = False
        buffer = []

        try:
            ipaddress.IPv4Network(cidr, strict=False)
            ans = True
        except ipaddress.AddressValueError as err:
            # ipaddress.AddressValueError: Octet 333 (> 255) not permitted in '10.33.333.254'
            pattern = """Octet \d+ \(.+\) not permitted in '\d+(\.\d+){3}'"""
            if not re.search(pattern, str(err)):
                buffer = ['Detected invalid address %s: %s' % (cidr, err)]
        except ipaddress.NetmaskValueError as err:            
            # ipaddress.NetmaskValueError: '255' is not a valid netmask
            buffer = ['Detected invalid netmask %s: %s' % (cidr, err)];
        except ValueError as err:
            print(" ** err: %s" % err)
        except Exception as err:
            buffer = ['Detected invalid argument %s: %s' % (cidr, err)]

        setattr(self, 'errors', buffer)
        return ans
    
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def is_valid_syntax(self, cidr) -> bool:
        """Detect if address string has valid syntax.

        :param cidr: cidr string to validate
        :type  cidr: str

        :return: Status based on detection.
        :rytpe: bool
        """

        valid_octet   = '255'

        # netmask == ipaddress._max_prefixlen()
        # ipaddress.NetmaskValueError: '255' is not a valid netmask        
        valid_netmask = '32' # '255' 
        
        parsed    = self.cidr_split(cidr)
        faux_ip   = '.'.join([valid_octet for octet in parsed['octets']])
        faux_cidr = "%s/%s" % (faux_ip, valid_netmask)
        return self.is_valid_cidr(faux_cidr)

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def is_valid(self, arg, show=None):
        """Determine if a command line argument is valid."""

        if show is None:
            show is False

        # if ipv6.validate_ip(addr):
        # if ipv4.validate_ip(addr):
        if not self.is_valid_syntax(arg):
            errs = ['Detected invalid cidr=%s' % arg]

        elif not self.is_valid_cidr(arg):
            errs = getattr(self, 'errors') # set by is_valid

        else:
            errs = []

        ans = True
        msg = ''
        if len(errs) != 0:
            ans = False
            msg = pprint.pformat({
                'iam'   : main_utils.iam(),
                'error' : '\n'.join(errs),
                'arg'   : arg,
                'exp'   : 'xx.xx.xx.xx/{bitmmask}'
            }, indent=4)
                
        setattr(self, 'error', msg)
        return len(msg) == 0
 
# [EOF]

            # network = ipaddress.IPv4Network((ip_200, mask), strict=False)
            # print(network)

        # https://python-iptools.readthedocs.io/en/latest/
