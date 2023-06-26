# -*- python -*-
"""Workflow templates used to abstract network configs"""

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import os
import pdb
import pprint

from pathlib     import Path
from string      import Template

class Utils:
    """A module for populating vlan templates."""

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, args=None):
        """Constructor.
        :param args: 
        """
        if args is None:
            args = {}

        for key,val in args.items():
            setattr(self, key, val)

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def fill_in(self, name, args) -> str:
        """Generate a string from a tempalte and arguments.

        :param name: Name of a template file to load.
        :type  name: str
        
        :param args: Values to populate a template with.
        :type  args: dict
        
        :return: A string buffer containing the populated tempalte
        :rtype : str

        Template is the name of a source workspace template.
        Args contains (keys:$replace_str) (vaLs:'replacement value').
        """

        # Construct path to template file
        path = Path(__file__).resolve().parent
        tmpl = path / name
        
        # Load and populate template
        config = None
        with open(tmpl, 'r', encoding='utf8') as workflow:
            stream = Template(workflow.read())
            config = stream.substitute(args).rstrip()
            config += '\n'

        return config
 
# [EOF]
