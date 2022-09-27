# -*- python -*-
"""This library is used to maintain header content on a spreadsheet."""

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import copy
import pprint

class HdrUtils:
    """ . """

    col = { 'value':None, 'letter':None }
    row = { 'value':None, 'letter':None }
    
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, row=None, col=None):
        """Constructor."""

        if row is not None:
            self.set(row=row)

        if col is not None:
            self.set(col=col)
            
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def set(self, col=None, row=None) -> None:

        if row is not None:
            rec = {'value' : row, 'letter' : str(row)}
            self.row = rec

        if col is not None:
            rec = {'value' : col, 'letter' : self.get_letter(col)}
            self.col = rec

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_letter(self, col) -> str:
        """Convert a column value into a spreadsheet letter.
        :param col: Column offset
        :type  col: int

        :return: Col convertd into a letter.
        :rytpe:  str
        """

        return chr(ord('A') + col - 1)            

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_address(self, row=None, col=None) -> str:

        row_rec = copy.copy(self.row)
        col_rec = copy.copy(self.col)

        if row is not None:
            row_rec['value']  = row
            row_rec['letter'] = str(row)
        
        if col is not None:
            col_rec['value']  = col
            col_rec['letter'] = self.get_letter(col)

        ans = "%s:%s" % (col_rec['letter'], row_rec['value'])

        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_range(self, row=None, col=None) -> str:

        start = self.get_address() # constructor args)
        if not row:
            ans = start
        else:
            # max_row, max_col for ranges
            end = self.get_address(row=row, col=col)
            ans = '%s,%s' % (start, end)

        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------  
    def get_header_raw_orig(self):
        """Return data structure that describes stats spreadsheet header row."""

        raw = [
            # -------------------------------------------------
            {
                'label':'DATE',     'width':11,
                'skip':True,
            },
            {
                # 'align':'right'
                'label':'TIME',     'width':11,
            } ,
            {
                'label':'DAY',      'width':5,
                'align':'center',
            },
            {
                'label':'',         'width':1,
                'skip':True,
            },
            # -------------------------------------------------
            {
                'label':'ACTIVE',   'width':2 + len('ACTIVE'),
            },
            {
                'label':'ENABLED',  'width':8,
            },
            {
                'label':'DISABLED', 'width':8,
            },
            {
                'label':'',         'width':1,
            },
            # -------------------------------------------------
            {
                'label':'SUCCESS',  'width':8,
            },
            {
                'label':'FAILURE',  'width':8,
            },
            {
                'label':'UNSTABLE', 'width': 2 + len('UNSTABLE'),
            },
            {
                'label':'ABORTED',  'width':8,
            },
            {
                'label':'',         'width':1,
            },
            # -------------------------------------------------
            {
                'label':'SFUA',     'width': 2 + len('UNSTABLE'),
            },
            {
                'label':'VIEW',     'width':6,
            },
            {
                'label':'URL',      'width':6,
            },
            {
                'label':'TOTAL',    'width':6,
            },
            {
                'label':'',         'width':1,
            },
            # -------------------------------------------------
            {
                'align':'left',
                'label':'NOTES', 'width':100,
            },
        ]

        def_none = ['align']
        def_bool = ['skip']
        def_list = []
        def_list += def_none
        def_list += def_bool
        
        # ------------
        # Add defaults
        # ------------ 
        headers = [] # accumulate non-skip records
        col = 1
        for header in raw:

            if 'skip' in header and header['skip']:
                continue

            header['col']        = col
            header['col-letter'] = chr(ord('A') + col - 1)
            
            # Apply defaults
            for key in def_list:
                if key in header.keys():
                    continue
                elif key in def_bool:
                    header[key] = False
                elif key in def_none:
                    header[key] = None
                    
            headers += [header]
            col = col + 1
                
        return headers

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------  
    def get_header_raw(self):
        """Return raw header data used to render a per-job stats spreadsheet."""

        raw = [
            # -------------------------------------------------
            {
                'label':'DATE',     'width':11,
                'skip':True,
            },
            {
                # 'align':'right'
                'label':'TIME',     'width':11,
            } ,
            {
                'label':'DAY',      'width':5,
                'align':'center',
            },
            {
                'label':'',         'width':1,
                'skip':True,
            },
            # -------------------------------------------------
            {
                'label':'ACTIVE',   'width':2 + len('ACTIVE'),
            },
            {
                'label':'ENABLED',  'width':8,
            },
            {
                'label':'DISABLED', 'width':8,
            },
            {
                'label':'',         'width':1,
            },
            # -------------------------------------------------
            {
                'label':'SUCCESS',  'width':8,
            },
            {
                'label':'FAILURE',  'width':8,
            },
            {
                'label':'UNSTABLE', 'width': 2 + len('UNSTABLE'),
            },
            {
                'label':'ABORTED',  'width':8,
            },
            {
                'label':'',         'width':1,
            },
            # -------------------------------------------------
            {
                'label':'SFUA',     'width': 2 + len('UNSTABLE'),
            },
            {
                'label':'VIEW',     'width':6,
            },
            {
                'label':'URL',      'width':6,
            },
            {
                'label':'TOTAL',    'width':6,
            },
            {
                'label':'',         'width':1,
            },
            # -------------------------------------------------
            {
                'align':'left',
                'label':'NOTES', 'width':100,
            },
        ]

        return raw

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------  
    def get_headers(self, raw:list=None):
        """Given basic spreadsheet header data populate the structure with defaults.

        :param raw: header data to format (label=, width=)
        :type  raw: dict

        :return: Header values sutible for spreadsheet rendering.
        :rtype : dict 
           align   left, center, right
           col     Index of column to render
           label   Column label
           skip    Exclude line item from rendering.
           width   Explicit column width (width=None will render to largest data value).
        """

        if raw is None:
            raw = self.get_header_raw()
            
        def_none = ['align']
        def_bool = ['skip']
        def_list = []
        def_list += def_none
        def_list += def_bool
        
        # ------------
        # Add defaults
        # ------------ 
        headers = [] # accumulate non-skip records
        col = 1
        for header in raw:

            if 'skip' in header and header['skip']:
                continue

            header['col']        = col 
            header['col-letter'] = self.get_letter(col)
            
            # Apply defaults
            for key in def_list:
                if key in header.keys():
                    continue
                elif key in def_bool:
                    header[key] = False
                elif key in def_none:
                    header[key] = None
                    
            headers += [header]
            col = col + 1
                
        return headers

# [EOF]
