#!/usr/bin/env python
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import unittest
import pprint

from pathlib           import Path

from vlan.main         import utils           as main_utils
from vlan.utils        import traverse
from vlan.utils        import views           as vu   # ViewUtils

class TestStringMethods(unittest.TestCase):
    
    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def test_get_address(self) -> list:

        obj = hdr.HdrUtils() 
        
        row = 65
        val = obj.get_address(row=row)
        self.assertEqual(val, row)

        data = {}
        for letter in ['A', 'J', 'Z']:
            data[letter]=\
                {
                    'col' : ord(letter),
                    'row' : row,
                    'chr' : letter,
                    'exp' : '%s:%d' % (letter, row),
                }

        for letter,rec in data.items():

            # Verify consistency of %exp
            for key in ['chr', 'col']:
                self.assertEqual(letter, rec[key])

            col = rec['col']
            val = get_address(col=col)
            self.assertEqual(val, rec['chr'])

            row = rec['row']
            val = get_address(row=row)
            self.assertEqual(val, rec['row'])

    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def test_get_range(self) -> list:
        
        obj = hdr.HdrUtils(row=2, col=5)
        val = obj.get_range()
        self.assertEqual(val, 'E:2')

        val = obj.get_range(row=10, col=5)
        self.assertEqual(val, 'E:2,J:5')
            
##----------------##
##---]  MAIN  [---##
##----------------##
if __name__ == '__main__':
    unittest.main()

# [EOF]
