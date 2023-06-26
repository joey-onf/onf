# -*- python -*-
'''.'''

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pprint
import semantic_version

# v = semantic_version.Version('0.1.1')
# import time
# import uuid
# >>> semantic_version.Version(major=0, minor=1, patch=2)
# Version('0.1.2')



from validate.main        import utils           as main_utils

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
class Data1:
    '''.'''

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self):
        '''Constructor.'''

        for key,val in args.items():
            setattr(self, key, val)

        return

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
class Data2:
    '''.'''
    
    hostname  = None

    # Constructor attrs are persistent, method args are transient
    debug = None
    trace = None
    verbose = None

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, hostname, args:dict=None, debug=None, trace=None):
        """Constructor.

        :param args: Arguments used to initialize object attributes.
        :type  args: dict, optional
        """

        ## TODO: Should be part of an inherited base class.
        if debug is None:
            debug = False
        if trace is None:
            trace = False

        self.debug = debug
        self.trace = trace

        if args is None:
            args = {}

        for key,val in args.items():
            setattr(self, key, val)

        return

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def foo(self, trace=None):
        # check_trace_mode(trace)
        pass

# -----------------------------------------------------------------------
# ..seealso: https://semver.org/
# ..seealso: https://python-semanticversion.readthedocs.io/en/latest/
# ..seealso: https://pypi.org/project/semver/
# -----------------------------------------------------------------------

# [EOF]
