# -*- python -*-
""" . """

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import sys
import pdb
import pprint

from pathlib           import PurePath, Path

import copy

import xml.etree.ElementTree as ET

from vlan.main         import utils as main_utils
from vlan.utils        import jenkins
from vlan.utils        import traverse

class ViewUtils:
    """ . """

    cached = {}

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, xml_dir, args=None):
        """Constructor.

        :param xml_dir: Filesystem xml_dir to XML data retrieved from jenkins.
        :type  xml_dir: str

        :param args: Attributes to initialize an object with.
        :type  args: dict, conditional
        """

        self.xml_dir = xml_dir

        if args is None:
            args = {}

        if 'view_method' not in args:
            args['view_method'] = 'dynamic'

        for key,val in args.items():
            setattr(self, key, val)

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

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_data_static(self, view:str=None) -> dict:
        """Retrieve a list of job names from jenkins xml view data.

        :return: XML data read from input file
        :rtype : dict

        ..todo: Support conditional load from restapi or cached on disk.
        ..todo: Accept view as arbitary args and return requested (a subset of view data).
        """

        iam = main_utils.iam()

        views = []
        if view is None:
            views += self.get_view_names()
        elif isinstance(view, str):
            views += [view]
        elif isinstance(view, list):
            views += view # TODO: flatten list-of-lists
        elif isinstance(view, dict):
            views += [ view.keys() ]
        else:
            err = "%s ERROR: Detected unhandled arg type:\n%s" \
                % pprint.pformat({
                    'type(view)' : type(view),
                    'view'       : view,
                }, indent=4)
            raise ValueError(err)

        ans = {}
        for view in views:
            if view not in self.cached:
                xml_file = Path(self.xml_dir + '/' + view)
                data = self.parseXML2(xml_file, ['name'], debug=False)
                self.cached[view] = data
            ans[view] = copy.copy(self.cached[view])

        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_data_dynamic(self, view:str=None) -> dict:
        return self.get_data_static(view)

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_view_data(self, view:str=None) -> dict:

        view_method = getattr(self, 'view_method')        

        return self.get_data_static(view) \
            if view_method == 'static' \
            else self.get_data_dynamic(view)

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_views_data(self, wanted=None) -> dict:
        """Return xml data for available jenkins views.

        :param wanted: When passed return a subset of view data.
        :type  wanted: list

        :return: View xml data key(d) by view name.
        :rtype:  dict
        """
        
        if wanted is None:
            wanted = [ self.get_view_names() ]

        ans = {}
        for view in wanted:
            ans[view] = get_view_data(view)

        return ans
    
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def parseXML2(self, xmlfile: str, wanted: list, debug=None):

        if debug is None:
            debug = False

        # create element tree object
        tree = ET.parse(xmlfile)
        # tree.dump()

        ans = {key:[] for key in wanted}
        for elem in tree.iter():

            if debug:
                pprint.pprint({
                    'attrib' : elem.attrib,
                    'tag'    : elem.tag,
                    'text' : elem.text,
                })

            if elem.tag in wanted:
                ans[elem.tag] += [elem.text]
                # print(" %s %s" % (elem.tag, elem.text))
            # p.elem.attrib.
            # {'_class': 'hudson.model.ListView'}

        return ans
    
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_job_names(self, view) -> list:
        """Return a list of job names associated with a view.

        :param view: Name of a jenkins view to retrieve data from.
        :type  view: str

        :return: A list of jenkins job names associated with a view.
        :rtype: list
        """

        rec = self.get_view_data(view=view)
        # ans = rec['name']
        ans = rec
        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_view_static(self) -> dict:
        """Generate a dictionary of view data by reading static xml data from disk files.
        """

        xml_dir = self.xml_dir

        ans = {}
        for xml_file in traverse.traverse(xml_dir):
            view = Path(xml_file).name
            data = self.parseXML2(xml_file, ['name'], debug=False)
            ans[view] = data['name']

        return ans
    
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_view_dynamic(self) -> dict:
        """
        ..todo: RestAPI query for data.
        """

        return self.get_view_static()
    
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_views(self) -> dict:
        '''Iterate and build a dictionary of jenkins view xml data.'''

        xml_dir = self.xml_dir
        views = self.get_view_names()

        ans = {}
        for view in views:
            rec = self.get_view_data(view)
            ans[view] = rec[view]

        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def job_to_view(self, job) -> dict:
        '''Given the name or path of a jenkins job map it into a jenkins view.

        :param job: A job path or name to lookup.
        :type  job: str

        :return: Jenkins view(s) the job belongs to.
        :rtype:  list
        '''

        job_name = PurePath(job).name

        xml_dir = self.xml_dir
        views = self.get_view_data()

        ans = []
        for view,rec in views.items():
            if job_name in rec['name']:
                ans += [view]

        return ans

    
    ## ----------------------------------------------------------------------- 
    ## -----------------------------------------------------------------------
    def xml_file(self, relpath) -> str:
        """Construct filesystem paths relative to the object root dir.

        :param relpath: Path to a retrieved jenkins view data file.
        :type  relpath: str

        :return: A filesystem path
        :rtype:  str
        """

        xml_file = Path(self.xml_dir + '/' + relpath)
        return xml_file.as_posix()  # ALT: str(xml_file)

# [EOF]
