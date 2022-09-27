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
    def get_job_by_log_dir(self) -> dict:
        """Gather a list of job filesystem paths via jenkins/logs
        
        :param src: Filesystem path that contains views/xml as a subdir.
        :type  src: str

        :return: Information about the current filesystem path.
        :rtype:  dict(via yield)
        """

        raise NotImplementedError( main_utils.iam() )
        
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_job_by_views_xml(self, src=None) -> dict:
        """Gather a list of job filesystem paths from views/xml.
        
        :param src: Filesystem path that contains views/xml as a subdir.
        :type  src: str

        :return: Information about the current filesystem path.
        :rtype:  dict(via yield)
        """

        ## [TODO]
        ##    o refactor with get_job()
        ##    o Pass as incl/excl filter lists
        argv = main_getopt.get_argv()
        if src is None:
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

            ans=\
                {
                    'name'   : job_name,
                    'path'   : job_path,
                    'views'  : mapped_views,
                }

            yield ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_job(self, method=None, src=None) -> dict:
        """Return a list of jobs based on traversal of views/xml.
        
        :param method: Gather job names by this method.
        :type  method: str, conditional

        :return: String name of the current jenkins job to process.
        :rtype : str

        ..todo: Refactor with get_job_by_views_xml()
        ..todo: Refactor with get_job_by_log_dir()
        ..todo: Pass argv[{job,view}_name] as {excl,incl}=[] filter lists.

        ..note: Filtering by views/xml will render current results.
        """

        valid = [ 'jekins/logdir', 'views/xml']
        
        if method is None:
            method = 'views/xml'

        if src is None:
            argv = main_getopt.get_argv()
            src  = argv['jenkins_dir']
        
        ans = None
        if method == 'views/xml':
            ans = self.get_job_by_views_xml(src)
        elif method == 'jenkins/logs':
            ans = self.get_job_by_log_dir(src)
        else: # not in valid
            raise ValueError("Detected invalid travseral mode [%s]" % mode)

        return ans
            
# [EOF]
