# -*- python -*-
'''.'''

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import random

from openpyxl.styles    import Color, PatternFill, Font, Border
from openpyxl.styles    import colors
from openpyxl           import Workbook

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
from stats.spreadsheet  import hdr             as sheet_hdr
from stats.spreadsheet  import elapsed         as onf_elapsed

class Elapsed:
    '''.'''

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def gen_tab(self, tab:str, debug:bool=None):

        if debug is None:
            debug = False

        work = Workbook()

        if 'Sheet' in work: # remove default
            work.remove(work['Sheet'])

        obj = sheet_hdr.Utils(work, tab)
        obj.generate_tab()

        summaries  = obj.get_summaries()
        min_max_es = obj.get_min_max_es()

        suites=\
            [
                'build_flex-ocp-cord-multi-uni_TP_TT_voltha_master',
                'build_flex-ocp-cord-multi-uni_TP_voltha_TT_master_test',
                'build_flex-ocp-cord_Default_voltha_master',
                'build_menlo-certification-pod-radisys-1600g_1T8GEM_DT_voltha_master',
                'periodic-software-upgrade-test-bbsim',
                'periodic-voltha-dt-fttb-test-bbsim',
                'periodic-voltha-multi-uni-test-bbsim',
            ]

        views=\
            [
                'VOLTHA-2.8',
                'VOLTHA-2.x-Tests',
                'OMEC',
                'voltha-scale-measurement',
                'voltha-soak',
            ]

        for row in range(3,50):
            data = {}
            for summary in summaries:
                data[summary] = {}
                for min_max in min_max_es:
                    data[summary][min_max] = random.randint(1, 255)
                    
            data['view']    = random.choice(views)
            data['suites']  = random.choice(suites)
                
            obj.set_row(row, data)
                
        work.save(filename='elapsed.xlsx')

# [EOF]
