# -*- python -*-
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
"""Derive indexes from a job stats data structure."""

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pprint

from vlan.jenkins       import iterator        as job_iterator

class IndexUtils:
    """."""

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
    def view_to_jobs(self, debug=None) -> dict:
        """
        :return: A mapping of jobs by jenkins view.
        :rytpe : dict

        ...note: expensive - filesystem traversal
        """

        if debug is None:
            debug = False

        ans = {}
        jit = job_iterator.JobUtils(attrs={})
        for job_meta in jit.get_job():

            if debug:
                pprint.pprint(job_meta)
            
            job_name = job_meta['name']
            for view in job_meta['views']:
                if view not in ans:
                    ans[view] = []
                ans[view] += [job_name]

        for key,val in ans.items():
            ans[key] = sorted(val)

        return ans
# [EOF]
