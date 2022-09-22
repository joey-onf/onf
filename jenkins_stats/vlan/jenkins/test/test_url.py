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

from vlan.jenkins      import url             as jurl
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
    def test_gen_job_url(self) -> str:

        # type view dir meta

        view = 'voltha-scale-measurements'
        job_meta=\
            {
                'job_id': '9511',
                'name': 'bbsim_scale_test',
#                'path': '/home/joey/projects/sandbox/onf/logs/var/lib/jenkins/jobs/bbsim_scale_test',
                'path': 'var/lib/jenkins/jobs/bbsim_scale_test',
                'views': [view],
            }

        urls = jurl.JenkinsUrls().gen_job_urls(job_meta)
        self.assertEqual(len(urls), 1)

        for val in [
                'bbsim_scale_test',
                '9511',
                'voltha-scale-measurements'
        ]:
            self.assertIn(val, urls[view])

        self.assertEqual(urls[view], '/'.join([
            'https://jenkins.opencord.org',
            'view/voltha-scale-measurements',
            'job/bbsim_scale_test',
            '9511/console',
        ]))
        
##----------------##
##---]  MAIN  [---##
##----------------##
if __name__ == '__main__':
    unittest.main()

# [EOF]
