# -*- python -*-
"""This module accumulates data for a host under inspection."""

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pprint
import time
import uuid

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

# [EOF]
