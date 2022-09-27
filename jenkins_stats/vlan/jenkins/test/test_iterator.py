#!/usr/bin/env python
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import unittest       #import TestCase
import pprint

from pathlib           import Path

from vlan.main         import utils           as main_utils
from vlan.main         import argparse        as main_getopt

from vlan.jenkins      import iterator        as job_iterator
from vlan.utils        import traverse

class TestStringMethods(unittest.TestCase):

    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def setUp(self):

        """Derive path to sandbox root to access other resources."""

        if False:
            raise Exception(' ** %s called' % main_utils.iam())

        top_rel = '../' * 3
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
    def set_test_argv(self):

        # jenkins_stats/../logs
        root = self.get_path_to_root()
        logdir = Path(root + '/../logs').resolve().as_posix()

        main_getopt.set_argv({
            'jenkins_dir' : logdir, 
            'job_name'    : [
                'bbsim_scale_test',
                'voltha-scale-measurements-master-10-stacks-2-16-32-dt-subscribers',
                'xos-data-model-scale',
            ],
            'view_name'   : [
                'Community-PODs',
                'voltha-scale-measurements',
            ],
        })
        
    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def get_path_to_root(self) -> str:
        path = getattr(self, 'path_to_root')
        return path
   
    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def test_get_job_meta(self):
        '''Verify behavior of jenkins job metadata retrieval funciton'''

        self.set_test_argv()

        ajv = ['All Jobs', 'voltha-scale-measurements']
        exp = {
            'bbsim_scale_test'\
                : ['All Jobs', 'voltha-scale-measurements'],
            'voltha-scale-measurements-master-10-stacks-2-16-32-att-subscribers'\
                : ['All Jobs', 'voltha-scale-measurements'],
        }

        
        job_stream = job_iterator\
            .JobUtils()\
            .get_job()

        exp_keys = exp.keys() # extract once
        for job_meta in job_stream:
            job_name = job_meta['name']

            if 'xos' in job_meta['path']:
                pprint.pprint(job_meta)
                import pdb
                pdb.set_trace()

            if job_name not in exp_keys:
                continue

            self.assertListEqual(sorted(job_meta['views']), exp[job_name])
        
##----------------##
##---]  MAIN  [---##
##----------------##
if __name__ == '__main__':
    unittest.main()

# [EOF]
