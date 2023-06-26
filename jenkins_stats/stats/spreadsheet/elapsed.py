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

    ws = None

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, wb, tab, debug=None, trace=None):
        '''Constructor.

        :param wb: A spreadsheet workbook to perform actions on.
        :type  wb: openpyxl.Workbook()

        :param tab: Name of a spreadsheet tab to create in workbook.
        :type  tab: str
        '''

        ## TODO: Should be part of an inherited base class.
        if debug is None:
            debug = False
        if trace is None:
            trace = False

        self.debug = debug
        self.trace = trace

        self.wb  = wb
        self.tab = tab
        
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
    def header(self):
        rec    = ['min', 'max', 'avg', 'count']
        fields = ['TOTAL', 'SUCESS', 'FAILURE', 'ABORT']
        columns = [ 'Suite', 'View', 'TOTAL', 'SUCCESS', 'FAILURE', 'ABORT', 'Description']

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def create(self):
        self.ws = workbook.create_sheet(title='elapsed')

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def do_header(self):
        """Given a data structure render a spreadsheet header.
        
        :param ws: Worksheet to generate a header for.
        :type  ws:
        
        :param header: A structure containing header data to render.
        :type  header:
        """

        ws = self.ws

#        ws = workbook.create_sheet(title=vx)
#        do_header(ws)      
#        sheet = Workbook().active
        
        row = ['foo', 'bar', 'tans', 'fans']
        col = [ range(1,3) ]
        cell = sheet.cell(row=row, column=col)

        cell.font = get_fonts('yellow')
        cell.fill = get_fills('purple')

        if col_max is None:
            col_max = 100

        col = 1 # for visiblity in col_fill floop
        for header in headers:
            if not 'col' in header:
                pprint.pprint(header)

            col   = header['col']
            label = header['label']
            width = header['width']
            align = header['align']        
            col_hdr(ws, col, label, width=width, align=align)

        for col_fill in range(col+1, col_max):
            col_hdr(ws, col_fill, '')

# [EOF]
