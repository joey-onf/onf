#!/usr/bin/env python
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
"""Gather jenkins job stats and render in a report."""

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pprint
import sys
import time

from pathlib import Path

import urllib.parse
from urllib.parse import urlunsplit, urljoin, urlencode

from vlan.main          import argparse        as main_getopt
from vlan.main          import help            as main_help
from vlan.main          import utils           as main_utils

from vlan.jenkins       import iterator        as job_iterator
from vlan.jenkins       import url             as jurl

from vlan.report        import to_stdout

from vlan.utils.consts  import \
    get_types_result,          \
    get_types_state,           \
    get_types_stat

from vlan.utils         import jenkins         as jenk_utils
from vlan.utils         import views           as vu
from vlan.utils         import spreadsheet
from vlan.utils         import traverse

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def init(debug=None):
    """Script initialization, verify interpreter version is sane."""

    if debug is None:
        debug = False

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def to_bool(val:str) -> bool:
    """HELPER: working cast for bool(str)"""

    return val.lower() in ['true', '1', 't', 'y', 'yes']

# config.xml
#  <disabled>false</disabled>

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def init_stats_rec(path:str) -> dict:
    """Define a standard storage rec for stats accumulation.
    :param path: Path to a jenkins job directory.
    :type  path: str

    :return: An initialized stats record.
    :rtype:  dict
    """

    stats   = get_types_stat()
    states  = get_types_state()
    results = get_types_result()

    ans = {}
    for key in stats + states + results:
        ans[key] = []

    ans['name'] = Path(path).name
    return ans

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def digest_args():
    """Perform actions based on command line args.

    :param argv: Command line args processed by python getopts
    :type  argv: dict

    :return: Success/failure set by action performed
    :rtype : bool
    """

    argv = main_getopt.get_argv()
    debug = argv['debug']

    stats_keys = ['job_views', 'job_dirs', 'job_totals']
    stats = { key:[] for key in stats_keys }

    my_stats = {}
    job_data = {}
    to_view  = {}
    with main_utils.pushd(argv['jenkins_dir']): # tempdir=True)

        ## ----------------------------------------------------
        ## Generate a data stream by traversing the filesystem
        ## gathering historical data from beneath jenkins jobs/
        ## ----------------------------------------------------
        jit = job_iterator.JobUtils(attrs={})

        for job_meta in jit.get_job():

            if debug:
                pprint.pprint(job_meta)
       
            job_name = job_meta['name']
            job_dir  = job_meta['path']
            my_stats[job_name] = init_stats_rec(job_name)
                
            # ------------------------------
            # Track job statistics;
            #   o total = enabled + disabled
            # ------------------------------
            jdu = jenk_utils.JobDirUtils(job_meta['path'])
            state = jdu.get_job_state()
            my_stats[job_name][state] += [job_name]
            my_stats[job_name]['permalinks'] = jdu.get_permalinks()

            job_data[job_name] = []

            # -------------------------------------
            # Gather per-job-invocation attributes:
            #   ABORTED, FAILURE, SUCCESS, UNSTABLE
            # -------------------------------------
            job_dirs = traverse.find_by_name(job_dir, ['build.xml'])
            for job_dir in job_dirs:

                job_id = Path(job_dir).name
                job_meta['job_id'] = job_id
                
                result = jenk_utils.JobDirUtils(job_dir).get_job_result()

                # -----------------
                # Job runtime stats
                # -----------------
                wanted  = ['queueId', 'result', 'duration', 'timestamp']                    
                runtime = jenk_utils\
                    .JobDirUtils(job_dir)\
                    .get_job_attrs(wanted)

                # ---------------------------------
                # Construct URLs for jenkins access
                # ---------------------------------
                urls = jurl.JenkinsUrls().gen_job_urls(job_meta)
                stats=\
                    {
                        'meta'    : job_meta,
                        'result'  : result,
                        'urls'    : urls,
                        'runtime' : runtime,
                    }
# -----------------------------------------------------------------------               
# {'bbsim_scale_test': [{'duration': '439300',
#                        'duration_hhmmss': '02:01:40',
#                        'id': '9511',
#                       'job_name': 'bbsim_scale_test',
#                       'month': 'Feb',
#                       'result': 'FAILURE',
#                       'timestamp': '1662991380452',
#                       'ts_ccyymmdd': '54668/02/06',
#                       'ts_hhmmss': '10:07:1662991398452',
#                       'urls': {'All Jobs': 'https://jenkins.opencord.org/view/All '
#                                            'Jobs/job/bbsim_scale_test/9511/console',
#                                'voltha-scale-measurements': 'https://jenkins.opencord.org/view/voltha-scale-measurements/job/bbsim_scale_test/9511/console'},
#                       'weekday': 'Thu'}]}
# -----------------------------------------------------------------------               

                ## --------------------------------------------------
                ## --------------------------------------------------
                duration     = runtime['duration']
                tg_duration  = time.gmtime( int(duration) )

                timestamp    = runtime['timestamp']
                tg_timestamp = time.gmtime( int(timestamp) )

                job_data[job_name] += [{
                    'job_id'    : job_id,
                    'job_name'  : job_name,
                    'result'    : result,
                    'urls'      : urls,        # { view : url }
                    #
                    'timestamp'       : timestamp,
                    'weekday'         : time.strftime('%a',        tg_timestamp),
                    'month'           : time.strftime('%b',        tg_timestamp),
                    'ts_ccyymmdd'     : time.strftime('%Y/%m/%d',  tg_timestamp),
                    'ts_hhmmss'       : time.strftime('%-H:%M:%s', tg_timestamp),
                    #
                    'duration'        : duration,
                    'duration_hhmmss' : time.strftime("%H:%M:%S", tg_duration)
                }]

                my_stats[job_name][result] += [stats]

    if argv['show']:
        to_stdout.ReportUtils().generate(my_stats)
        # show_report(my_stats)

    if argv['spreadsheet']:
        work = spreadsheet.gen_spreadsheet(my_stats, job_data)
        work.save(filename=argv['spreadsheet'])

    return

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def main(argv_raw):
    """Off to the races."""

    iam = main_utils.iam()
    debug = False
    if debug:
        print(" ** %s: BEGIN" % iam)

    init()
    main_getopt.getopts(argv_raw)
    digest_args()

##----------------##
##---]  MAIN  [---##
##----------------##
if __name__ == "__main__":
    main(sys.argv[1:]) # NOSONAR

# [EOF]
