#!/usr/bin/env python

#!/usr/bin/env python

import vlan.network.VlanUtils                  as vu

import unittest

class TestStringMethods(unittest.TestCase):

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def test_is_valid_cidr_FAIL(self):

        vu = vu_mod.VlanUtils()
        for cidr in\
            [
                '10.11.str.254/24',  # Are labels usable ?
                '10.11.111.254/255', # Invalid netmask
            ]:
            self.assertFalse( vu.is_valid_cidr(cidr), "CIDR: %s" % cidr)

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def test_is_valid_cidr_PASS(self):
        vu = vu_mod.VlanUtils()
        for cidr in\
            [
                '10.11.111.254/24',
                '10.33.333.254/24' # invalid octet (333>255)
            ]:
            self.assertTrue( vu.is_valid_cidr(cidr), "CIDR: %s" % cidr)

##----------------##
##---]  MAIN  [---##
##----------------##
if __name__ == '__main__':
    unittest.main()

# [EOF]
