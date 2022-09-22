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
from vlan.utils        import views           as vu   # ViewUtils

class TestStringMethods(unittest.TestCase):

    ## Class vars
    cached = {}

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
    def exp_voltha_view_names(self) -> list:
        exp = [
            'ci-management', 
            'Community-PODs',
            'VOLTHA 2.x verify',
            'VOLTHA-2.8',
            'VOLTHA-2.X-Tests',
            'voltha-scale-measurements',
            'voltha-soak',
        ]
        return exp

    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def exp_voltha_job_names(self) -> dict:
        return \
            {
                'ci-management': 'ci-management-ami-packer-merge-ubuntu-18.04-basebuild_1804',
                'Community-PODs': 'build_berlin-community-pod-1-gpon-adtran_1T8GEM_DT_voltha_2.8',
                'VOLTHA 2.x verify': 'verify_bbsim_licensed',
                'VOLTHA-2.8': 'build_flex-ocp-cord_1T4GEM_voltha_2.8',
                'VOLTHA-2.X-Tests': 'build_flex-ocp-cord-multi-uni_TP_TT_voltha_master',
                'voltha-scale-measurements': 'bbsim_scale_test',
                'voltha-soak': 'build_onf-soak-pod_1T8GEM_DT_soak_Func_voltha_2.8_manual_test',
            }
    
    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def test_get_view_names_by_xml_dir(self):
        """Verify name list by filesystem collection."""

        iam  = main_utils.iam()

        root = self.get_path_to_root()
        xml_dir = root + '/views/xml'

        got = vu.ViewUtils(xml_dir).get_view_names()
        got = sorted(got, key = lambda s: s.casefold())
        exp = self.exp_voltha_view_names()
        self.assertListEqual(got, exp,\
                        '%s ERROR: Collection failed %s' % (iam, xml_dir))

    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def test_get_views(self):
        ''' . '''

        root = self.get_path_to_root()
        xml_dir = root + '/views/xml'

        got = vu.ViewUtils(xml_dir).get_views()

        # Basic check: Verify gathered view names.
        got_names = sorted(got.keys(), key = lambda s: s.casefold())
        exp_names = self.exp_voltha_view_names()
        self.assertListEqual(got_names, exp_names,\
                        'get_views ERROR: Invalid view name(s) detected')

        # Room for improvement:
        #   o perform simple existence test for now.
        #   o maintain hardcoded comparison lists, jobs change is infrequent.
        exp_job_names = self.exp_voltha_job_names()
        for view,exp in exp_job_names.items():
            rec = got[view]['name']
            self.assertIn(exp, rec, pprint.pformat({
                'error' : 'get_views ERROR: view lacks jobname',
                'view' : view,
                'exp'  : exp,
                'got'  : rec,
            }, indent=4))

    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def test_get_views_data(self):
        ''' . '''

        root = self.get_path_to_root()
        xml_dir = root + '/views/xml'

        names = ['Community-PODs', 'voltha-soak']
        got = {}
        total = 0
        for view in names:
            got[view] = vu.ViewUtils(xml_dir).get_view_data(names)
            total = total + 1

        gots = vu.ViewUtils(xml_dir).get_view_data(names)
        self.assertEqual(len(gots), total)
        pprint.pprint({
            'total' : total,
        })
        
    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def disabled_test_get_view_methods(self):
        ''' . '''

        root = self.get_path_to_root()
        xml_dir = root + '/views/xml'

        exp_names = self.exp_voltha_view_names()

        constructor_attrs=\
            [
                { 'view_method' : 'static' },
                { 'view_method' : 'dynamic' },
                { 'view_method' : '' },
                { 'view_method' : 'invalid-is-dynamic' },
            ]

        for attrs in constructor_attrs:
            got = views\
                .ViewUtils(xml_dir,attrs)\
                .get_views('voltha-soak')

            got = sorted(got, key = lambda s: s.casefold())
            self.assertListEqual(got, exp)
        
    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def test_get_job_names(self):
        ''' . '''

        root = self.get_path_to_root()
        xml_dir = root + '/views/xml'

        # got = vu.ViewUtils(xml_dir).get_view_names()
        got = vu.ViewUtils(xml_dir).get_views()

        # Basic check: Verify gathered view names.
        got_names = sorted(got.keys(), key = lambda s: s.casefold())
        exp_names = self.exp_voltha_view_names()
        self.assertListEqual(got_names, exp_names,\
                        'get_views ERROR: Invalid view name(s) detected')

        # Room for improvement:
        #   o perform simple existence test for now.
        #   o maintain hardcoded comparison lists, jobs change is infrequent.
        exp_names = self.exp_voltha_job_names()
        for view,exp in exp_names.items():
            rec = got[view]
            self.assertIn(exp, rec['name'], pprint.pformat({
                'error' : 'get_views ERROR: view lacks jobname',
                'view' : view,
                'exp'  : exp,
                'got'  : got,
            }, indent=4))
            
##----------------##
##---]  MAIN  [---##
##----------------##
if __name__ == '__main__':
    unittest.main()

# [EOF]
