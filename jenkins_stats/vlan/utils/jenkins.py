# -*- python -*-
""" . """

##-------------------##
##---]  GLOBALS  [---##
##-------------------##
import sys

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pdb
import pprint

from pathlib           import Path

import xml.etree.ElementTree as ET

from vlan.utils        import traverse
from vlan.main         import utils as main_utils

class JobDirUtils:
    """ . """

    job_dir = None

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, job_dir, args=None):
        """Constructor.

        :param job_dir: Filesystem path containing a job directory.
        :type  job_dir: str

        :param args: Attributes to initialize an object with.
        :type  args: dict, conditional
        """

        self.job_dir = str(job_dir)
        
        if args is None:
            args = {}

        for key,val in args.items():
            setattr(self, key, val)

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def to_bool(self, val:str) -> bool:
        """HELPER: working cast for bool(str)"""

        return val.lower() in ['true', '1', 't', 'y', 'yes']

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_permalinks(self) -> dict:
        """Return contents of a job permalink file.
        :return: Content read from the permalink file.
        :rtype:  dict
        """

        ans = {
            'lastCompletedBuild'    : None,
            'lastFailedBuild'       : None,
            'lastStableBuild'       : None,
            'lastSuccessfulBuild'   : None,
            'lastUnstableBuild'     : None,
            'lastUnsuccessfulBuild' : None,
        }

        path = Path(self.job_dir + '/builds/permalinks')

        with open(path, 'r', encoding='utf-8') as stream:
            for line in stream:
                fields = line.rstrip().split(' ')
                if 2 != len(fields):
                    raise Exception("ERROR: Failed to parse %s [%s]" % (path, line))
                key,val = fields
                ans[key] = int(val)
                
        return ans

#  <queueId>17819</queueId>
#  <timestamp>1663178580447</timestamp>
#  <startTime>1663178580451</startTime>
#  <result>FAILURE</result>
#  <duration>429561</duration>
#  <charset>UTF-8</charset>
#  <keepLog>false</keepLog>
#  <execution class="org.jenkinsci.plugins.workflow.cps.CpsFlowExecution">
#    <result>FAILURE</result>
#    <script>/*

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_job_state(self) -> str:
        """ . """

        config_xml = Path(self.job_dir + '/config.xml')
        wanted = ['disabled']
        rec = self.parseXML(config_xml, wanted)

        ans = 'DISABLED' if self.to_bool(rec['disabled']) else 'ENABLED'
        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_job_result(self) -> str:
        """Retrieve result type for a given job

        .. todo: Replace hardcoded list with get_types_result()
        :return: an element from get_types_result()
        :rytpe : str
        """

        results = ['ABORTED', 'FAILURE', 'SUCCESS', 'UNSTABLE']

        build_xml = '/'.join([self.job_dir, 'build.xml'])
        rec = self.parseXML(build_xml, ['result'])

        if 'result' not in rec:
            raise Exception("Unable to detect <result>X</result> in %s" % build_xml)

        elif rec['result'] not in results:
            got = 'Found result [%s]' % result
            exp = 'expected %s' % ' '.join(results)
            loc = 'in file %s' % build_xml
            raise Exception("%s %s %s" % (got, exp, loc))

        ans = rec['result']
        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_job_attrs(self, wanted:dict) -> dict:

        build_xml = '/'.join([self.job_dir, 'build.xml'])
        ans = self.parseXML(build_xml, wanted)
        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def parseXML(self, xmlfile: str, wanted: list, debug=None):

        if debug is None:
            debug = False

        # create element tree object
        tree = ET.parse(xmlfile)
        # tree.dump()

        ans = {}
        for elem in tree.iter():

            if elem.tag in wanted:
                ans[elem.tag] = elem.text
                # print(" %s %s" % (elem.tag, elem.text))
            # p.elem.attrib.
            # {'_class': 'hudson.model.ListView'}

        return ans
            
# [EOF]
