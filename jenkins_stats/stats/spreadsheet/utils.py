# -*- python -*-
'''.'''

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import contextlib
import pprint

from pathlib import Path

from openpyxl          import Workbook
from openpyxl.worksheet.worksheet \
                       import Worksheet


class Utils:
    '''.'''

    wb  = None
    
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    @contextlib.contextmanager
    def new_spreadsheet(self, path:str): # -> openpyxl.workbook.workbook.Workbook:
        '''Define a context for creating a spreadsheet.

        Usage:
        with new_spreadsheet() as wb:
            wb.create_tab('elasped')
        '''

        self.wb = None

        wb = None
        try:
            wb = Workbook()
#            if 'Sheet' in wb:
#                wb.remove(wb['Sheet'])
            self.wb = wb
            yield wb

        finally:
            wb.save(filename=path)
       
# [EOF]
