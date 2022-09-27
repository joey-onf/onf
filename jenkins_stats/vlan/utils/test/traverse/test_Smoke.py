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
# from unittest          import TestCase
import pprint

from pathlib           import Path

from vlan.main         import utils           as main_utils
from vlan.utils        import traverse

class TestStringMethods(unittest.TestCase):

    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def setUp(self):

        """Derive path to sandbox root to access other resources."""

        if False:
            raise Exception(' ** %s called' % main_utils.iam())

        top_rel = '../' * 4
        test_dir     = Path(__file__).resolve().parent.as_posix()
        abs_path_rel = '/'.join([test_dir, top_rel])

        path_to_root = Path(abs_path_rel).resolve().as_posix()

        key  = 'path_to_root'
        setattr(self, key, path_to_root)
        
        return
    
    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def tearDown(self):
        """Sanity check env during destructor call."""

        if False:
            raise Exception(' ** %s called' % main_utils.iam())
        
        key  = 'path_to_root'
        self.assertTrue(hasattr(self, key), '%s= is undefined' % key)
    
    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def get_path_to_root(self) -> str:
        path = getattr(self, 'path_to_root')
        return path

    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def test_traverse(self):
        """Verify basic filesystem collection behavior."""

        # iam  = main_utils.iam()
        root = self.get_path_to_root()
        xml_files = traverse.traverse(root + '/views/xml')

        xml_file_names = [Path(path).name for path in xml_files]
        self.assertTrue('voltha-scale-measurements' in xml_file_names)
        self.assertEqual(len(xml_files), 23, 'Invalid VOLTHA xml view count detected')

##----------------##
##---]  MAIN  [---##
##----------------##
if __name__ == '__main__':
    unittest.main()

# [EOF]
