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
import sys

from vlan.utils         import consts

#class ToStdout:
class ReportUtils:
    """ . """

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__X(self, xml_dir, args=None):
        """Constructor.

        :param xml_dir: Filesystem xml_dir to XML data retrieved from jenkins.
        :type  xml_dir: str

        :param args: Attributes to initialize an object with.
        :type  args: dict, conditional
        """

        if args is None:
            args = {}

        for key,val in args.items():
            setattr(self, key, val)

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def generate(stats):
        """Render a text report to stdout."""

        print("""
## ---------------------------------------------------------------------------
## Job Summary
## ---------------------------------------------------------------------------
""")

        for view,rec in stats.items():
            print("[JOB] %s" % rec['name'])

            total = 0
            for key in consts.get_types_state():
                count = len(rec[key])
                total += count
                print("  %-14s: %d" % (key, count))
                print("  %-14s: %d\n" % ('', total))

            total = 0
            for key in consts.get_types_result():
                count = len(rec[key])
                total += count
                print("  %-14s: %d" % (key, count))
                print("  %-14s: %d\n" % ('', total))
            
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_view_names(self) -> list:
        '''Return a list of static view names retrieved from a local xml/ dir.

        :return: A static list of jenkins view names.
        :rtype:  list
        '''

        paths = traverse.traverse(self.xml_dir)
        ans = [Path(path).name for path in paths]
        return ans

# [EOF]
