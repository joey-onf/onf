# -*- python -*-
"""This library is used to maintain header content on a spreadsheet."""

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pprint
import random

from stats.tab         import elapsed     as tab_elapsed


## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
class Template:
    '''.'''

    tab = 'FIX_ME'
    wb  = None
    ws  = None

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, wb, tab:str):

        self.wb  = wb

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def prepare(self):
        pass

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def generate(self):
        pass


## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
class Elapsed:
    '''Generate a jenkins job elapsed stats spreadsheet tab.'''

    tab = None
    wb  = None
    ws  = None

    suites   = None
    stats    = None
    disabled = {}

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def __init__(self, wb, tab:str):

        self.wb  = wb
        self.tab = tab

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def init_summary(self):
        ans=\
            {
                'count':0 ,
                'duration': 0,
                'duration_hhmmss': '',
            }
        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def init_summaries(self):
        '''Create empty storage structure for stats records.

        :return: A structure for storing TOTALS, SUCCESS, FAILURE job stats.
        :rtype: dict
        '''

        summaries = tab_elapsed.Utils(None, 'elapsed').get_summaries()

        ans = {}
        for summary in summaries:
            ans[summary] = self.init_summary()
        return ans

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def calc_summaries(self, recs:list):
        '''Calculate elapsed stats for the first 5 spreadsheet tabs.

        :return: A stats structure containign TOTALS, SUCCESS, FAILURE, ...
        :rtype:  dict
        '''

        ans = self.init_summaries()
        for rec in recs:
            # 'duration': '5082',
            # 'duration_hhmmss': '1:24:42',
            for stat in ['TOTAL', rec['result']]:
                ref = ans[stat]
                ref['count']    = ref['count'] + 1
                ref['duration'] = ref['duration'] + int(rec['duration'])

        return ans
        
    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
    def prepare(self, stats:dict, jenkins:dict, debug:bool=None):

        logs = { 'stats.log' : stats, 'jenkins.log' : jenkins }
        for path,data in logs.items():
            with open(path, mode='w', encoding='utf-8', newline='') as stream:
                pp = pprint.PrettyPrinter(indent=4, compact=False)
                stream.write(pp.pformat(data))

        # Gathered
        suites   = []
        disabled = {}
        stats    = {}

        for suite,recs in jenkins.items():
            suites += [suite]
            total = self.init_summary()

            print(" ** suite: %s" % suite)
            if len(recs) == 0:
                print(" ** HUH: No records detected for %s" % suite)
                disabled[suite] = True
                continue
            

            disabled[suite] = bool(any([ rec['state'] \
                                         for rec in recs \
                                         if rec != 'ENABLED']))

            summaries = self.calc_summaries(recs)
            pprint.pprint({
                'suite'     : suite,
                'disabled'  : disabled,
                'summaries' : summaries,
            })

            next_suite = True

        self.suites   = suites
        self.disabled = disabled
        self.stats = stats

        return self

    ## -----------------------------------------------------------------------
    ## -----------------------------------------------------------------------
#    def generate(self, stats:dict, jenkins:dict, debug:bool=None):
    def generate(self, debug:bool=None):

        if debug is None:
            debug = False

        wb  = self.wb
        tab = self.tab

        obj = tab_elapsed.Utils(wb, tab)
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

        suites = self.suites
        disabled = self.disabled
        stats = self.stats

   
        import pdb
        pdb.set_trace()
        
        for row in range(3,50):
            for suite in suites:
                data = {}
                for summary in summaries:
                    data[summary] = {}
                    for min_max in min_max_es:
                        data[summary][min_max] = random.randint(1, 255)
                        
                        data['view']    = random.choice(views)
                        data['suites']  = random.choice(suites)

            obj.set_row(row, data)

        return self
   
# [EOF]
