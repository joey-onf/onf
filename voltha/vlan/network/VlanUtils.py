 # -*- python -*-
"""This module is used to derive network configs from CIDR(s)"""

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
    """This module is used to derive network configs from CIDR(s)"""

    error  = None
    errors = []

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, args=None):
        """Constructor.

        :param args: Arguments used to initialize object attributes.
        :type  args: dict, optional
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
            addr   - IP address as a string
            mask   - network mask
            octets - IP address split into a list of octets
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
    def is_valid_cidr(self, cidr) -> bool:
        """Validate --cidr command line argument value.

        :param cidr: 
        :type  cidr: str

        :return: True if string resembles a valid CIDR.
        :rtype : bool

        NOTE: Values accepted may not represent a valid network address.

          VLAN ID is passed as a CIDR value (invalid octet: x>=256)
          ---------------------------------------------------------
          VLAN 0,4095    - Reserved VLANs
          VLAN 1         - Default switch VLAN (RO)
          VLAN 2-1001    - User defined VLANs.
          VLAN 1002-1005 - CISCO defaults for fddi and token ring.
          VLAN 1006-4094 - Extended VLAN range.
        """

        ans = False
        buffer = []

        try:
            ipaddress.IPv4Network(cidr, strict=False)
            ans = True

        except ipaddress.AddressValueError as err:
            # Octet 333 (> 255) not permitted in '10.33.333.254'
            pattern = """Octet \d+ \(.+\) not permitted in '\d+(\.\d+){3}'"""
            if not re.search(pattern, str(err)):
                buffer = ['Detected invalid address %s: %s' % (cidr, err)]
            # elif octet >= 4096:

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
    def is_valid_octets(self, cidr) -> bool:
        """Determine if CIDR octet fields are valid.

        :param cidr: cidr string to validate
        :type  cidr: str

        :return: Status based on detection.
        :rytpe: bool
        """

        buffer = []
        parsed = self.cidr_split(cidr)
        for octet in parsed['octets']:
            if not octet.isdigit():
                buffer = ['Detected non-numeric octet: %s' % octet]
            elif int(octet) > 4095:
                buffer = ['Detected invalid vlan id (%s>4095): %s' % octet]
            elif int(octet) < 0:
                buffer = ['Detected invalid octet: %s' % octet]

        setattr(self, 'errors', buffer)
        ans = len(buffer) == 0
        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def is_valid_syntax(self, cidr) -> bool:
        """Detect if address string has valid syntax.

        :param cidr: cidr string to validate
        :type  cidr: str

        :return: Status based on detection.
        :rytpe: bool

        NOTE: Detection will preserve basic structure of the cidr argument
          but will replace values with a known valid octet.
        """

        valid_octet   = '255'
        valid_netmask = '32'
        
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

        elif not self.is_valid_octets(arg):
            errs = getattr(self, 'errors')

        elif not self.is_valid_octets(arg):
            errs = getattr(self, 'errors')

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

# [SEE ALSO]
# -----------------------------------------------------------------------
# ..seealso: https://www.geeksforgeeks.org/virtual-lan-vlan/
# ..seealso: https://python-iptools.readthedocs.io/en/latest/
# -----------------------------------------------------------------------
# network = ipaddress.IPv4Network((ip_200, mask), strict=False)
# print(network)
# -----------------------------------------------------------------------

# [EOF]
