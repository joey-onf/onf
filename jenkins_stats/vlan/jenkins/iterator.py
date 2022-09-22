# -*- python -*-
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
""" . """

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pdb
import pprint

from pathlib            import PurePath, Path

from vlan.main          import utils                   as main_utils
from vlan.main          import argparse                as main_getopt
from vlan.utils         import traverse
from vlan.utils         import views                   as vu

class JobUtils:
    """ . """

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, attrs=None):
        """Object constructor

        :param argv: Command line arguments processed by argparse.
        :type  argv: dict

        :param attrs: Attributes to initilize object with.
        :type  attrs: dict
        """

        if attrs is None:
            attrs = {}

        for key,val in attrs.items():
            setattr(self, key, val)

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_root_dir(self)->str:
        """Return path to the sandbox root directory based on module."""

        top = '../..'
        root = Path(__file__).resolve()\
                             .parent\
                             .parent\
                             .parent\
                             .as_posix()
        return root

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_job(self) -> dict:

        argv = main_getopt.get_argv()
        src  = argv['jenkins_dir']

        argv_jobs  = argv['job_name']        
        argv_views = argv['view_name']        

        root    = self.get_root_dir()
        xml_dir = Path(root + '/views/xml').resolve().as_posix()

        vobj = vu.ViewUtils(xml_dir)

        # Gather jobs path server path
        jenkins_jobs = traverse.find_by_jobdir(src)

        for job_path in jenkins_jobs:

            job_name = Path(job_path).name
            
            # Map job to containing view(s)
            mapped_views = vobj.job_to_view(job_path)

            ## --------------------------------------------
            ## Filter report by command line --view-name(s)
            ## --------------------------------------------
            if len(argv_views) > 0:
                overlap = set.intersection(set(mapped_views), set(argv_views))
                if len(overlap) == 0:
                    continue

            ## -------------------------------------------
            ## Filter report by command line --job-name(s)
            ## -------------------------------------------
#            if len(argv_jobs) > 0:
#                if job_name not in argv_jobs:
#                    continue

            ans=\
                {
                    'name'   : job_name,
                    'path'   : job_path,
                    'views'  : mapped_views,
                }

            yield ans

# [EOF]
