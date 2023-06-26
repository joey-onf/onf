#!/usr/bin/env python
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
'''A library for calculating elapsed runtime stats.'''

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pprint
from statistics import mean, median

class Elapsed():
    """ . """

    # Constructor attrs are persistent, method args are transient
    debug = None
    trace = None

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, debug=None, trace=None):
        '''Constructor.'''

        ## TODO: Should be part of an inherited base class.
        if debug is None:
            debug = False
        if trace is None:
            trace = False

        self.debug = debug
        self.trace = trace

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def do_trace_mode(self, trace=None):

        ## TODO: Should be part of an inherited base class.
        if trace is None:
            trace = self.trace
        if trace:
            import pdb
            pdb.set_trace()

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def gen_stats(self, elapsed:list) -> dict:
        '''Calculate summary stats for elapsed job runtime.'''

        self.do_trace_mode()

        ans=\
            {
                'count' : len(elapsed),
                'mid'   : None,
                'min'   : None,
                'max'   : None,
                'sum'   : sum(elapsed),
                'mean'  : None,
            }

        # _duration  = time.gmtime( int(duration) )
        
        if len(elapsed) > 0:
            ans['mid'] = median(elapsed)
            ans['min'] = min(elapsed)
            ans['max'] = max(elapsed)
            ans['avg'] = int(mean(elapsed))  # should ignore min/max for accuracy
        
        return ans
    
# [EOF]
