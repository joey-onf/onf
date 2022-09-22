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
from collections        import namedtuple
from urllib.parse       import urljoin, urlencode, urlparse, urlunparse

from vlan.main          import utils                   as main_utils

class JenkinsUrls:
    """ . """

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, attrs=None):
    # def __init__(self, https, attrs=None):
        """Object constructor
 
        :param attrs: Command line arguments processed by argparse.
        :type  attrs: dict
            https   Jenkins web URL https + server prefix.
            server  Jenkins server name

        :param attrs: Attributes to initilize object with.
        :type  attrs: dict
        """

        if attrs is None:
            attrs = {}

        if 'server' not in attrs:
            server = 'opencord'
            attrs['server'] = 'jenkins.opencord.org'

        if 'server' not in attrs:
            raise Exception('server= is required (jenkins.opencord.org)')

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
    def gen_job_url\
        (
            self,
            job_view,
            job_dir,
            job_meta,
            url_type=None,
            debug=None
        ) -> str:
        """Generate a web url from arguments.

        :param url_type: [console]
        :type  url_type: str

        :param job_view: Name of jenkins view to render a url for
        :type  job_view: str
        ex: voltha-scale-measurements

        :param job_meta: Summary of content and detail for a job.
        :type  job_meta: str
           ex: job_dir=var/lib/jenkins/jobs/bbsim_scale_test/builds/9511

        :param debug: Enable debug mode
        :type  debug: bool, conditional
        """
        
        if debug is None:
            debug = False

        if url_type is None:
            url_type = 'console'

        # https://jenkins.opencord.org/view/
        #   voltha-soak/
        #   job/build_onf-soak-pod_1T8GEM_DT_soak_Func_voltha_master_manual_test/
        #   35/console
 
        # namedtuple to match the internal signature of urlunparse
        Components = namedtuple\
            (
                typename    = 'Components', 
                field_names = ['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
            )
       
        view_str = 'view/%s'    % job_view
        job_str  = 'job/%s'     % job_meta['name']
        id_str   = '%s/console' % job_meta['job_id']
        
        url = urlunparse\
            (
                Components\
                (
                    scheme   = 'https',
                    netloc   = getattr(self, 'server'),
                    query    = None, # urlencode(query_params),
                    path     = None, # '{path}',
                    url      = "%s/%s/%s"  % (view_str, job_str, id_str),
                    fragment = None, # 'anchor'
                )
            )

        return url

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def gen_job_urls(self, job_meta, url_type=None) -> dict:
        """Generate a list of jenkins web urls from arguments.

        :param job_meta: A dictionary of parameters used for URL construction.
        :type  job_meta: dict

        :return: Jenkins web URLs keyed by view name.
        :rtype : dict
        """

        ans = {}
        for view in job_meta['views']:
            url = self.gen_job_url\
                (
                    view,
                    job_meta['path'],
                    job_meta,                    
                    url_type=url_type
                )
            ans[view] = url

        return ans

# [EOF]
