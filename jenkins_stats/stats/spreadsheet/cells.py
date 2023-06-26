# -*- python -*-
'''.'''

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
from openpyxl.styles    import Color, PatternFill, Font, Border
from openpyxl.styles    import colors

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import copy


class Posn:
    '''.'''

    col = { 'value':None, 'letter':None }
    row = { 'value':None, 'letter':None }
    ws = None

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, sheet=None, row:list=None, col:list=None):
        """Constructor.

        :param sheet: A spreadsheet workbook to perform actions on.
        :type  sheet: openpyxl.Worksheet, conditional
        """

        if sheet is not None:
            self.ws = sheet

        if row is not None:
            self.set(row=row)

        if col is not None:
            self.set(col=col)
            
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def get_sheet_required(self):

        sheet = self.ws
        if sheet is None:
            raise Exception("sheet= is required")
        return sheet

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def set(self, col=None, row=None) -> None:

        if row is not None:
            rec = {'value' : row, 'letter' : str(row)}
            self.row = rec

        if col is not None:
            letter = self.get_letter(col)
            rec = {'value' : col, 'letter' : letter}
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
    def col_range(self, row:int=None, col:int=None, width:int=None, tab:str=None) -> str:
        '''Generate an A1:B2 cell range for applying attributes.'''

        sheet = self.get_sheet_required()

        if row is None:
            row = cell.row_idx
        if col is None:
            col = sheet.cell.col_idx
        if width is None:
            width = 100  # make it obvious

        start = self.get_address(row=row, col=col)
        end   = self.get_address(row=row, col=col + width)

        col0 = start.replace(':', '')
        col1 = end.replace(':', '')
        ans = "%s:%s" % (col0, col1)
        return ans

# [EOF]
