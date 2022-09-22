#!/usr/bin/env python
"""Simple script to digest command line args."""

##-------------------##
##---]  GLOBALS  [---##
##-------------------##
# persist = None

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import pdb
import pprint
import sys

from pathlib import Path

import urllib.parse
from urllib.parse import urlunsplit, urljoin, urlencode

# import memcache

from vlan.main          import utils           as main_utils
from vlan.main          import help            as main_help

from vlan.jenkins       import iterator        as job_iterator
from vlan.jenkins       import url             as jurl

from vlan.utils         import jenkins         as jenk_utils
from vlan.utils         import views           as vu
from vlan.utils         import spreadsheet
from vlan.utils         import traverse
from vlan.main          import argparse        as main_getopt

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def init(debug=None):
    """Script initialization, verify interpreter version is sane."""

    if debug is None:
        debug = False

#     persist = memcache.Client(['127.0.0.0.1:11211', debug=0)

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def to_bool(val:str) -> bool:
    """HELPER: working cast for bool(str)"""

    return val.lower() in ['true', '1', 't', 'y', 'yes']

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def get_types_result() -> list:
    return ['ABORTED', 'FAILURE', 'SUCCESS', 'UNSTABLE']

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def get_types_state() -> list:
    return ['DISABLED', 'ENABLED']

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def get_types_stat() -> list:
    return ['jobs', 'total']

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def show_report(stats):

    print("""
## ---------------------------------------------------------------------------
## Job Summary
## ---------------------------------------------------------------------------
""")

    for view,rec in stats.items():
        print("[JOB] %s" % rec['name'])

        total = 0
        for key in get_types_state():
            count = len(rec[key])
            total += count
            print("  %-14s: %d" % (key, count))
        print("  %-14s: %d\n" % ('', total))

        total = 0
        for key in get_types_result():
            count = len(rec[key])
            total += count
            print("  %-14s: %d" % (key, count))
        print("  %-14s: %d\n" % ('', total))

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

            # -------------------------------------
            # Gather per-job-invocation attributes:
            #   ABORTED, FAILURE, SUCCESS, UNSTABLE
            # -------------------------------------
            job_dirs = traverse.find_by_name(job_dir, ['build.xml'])

            for job_dir in job_dirs:

                job_meta['job_id'] = Path(job_dir).name

                # -------------------------------------
                # total[1] = disabled + enabled
                # total[2] = aborted + passed + failed
                # total[1] == total[2]
                # -------------------------------------
                # {
                # 'queueId': '17371',
                # 'timestamp': '1662991380452',
                # 'result': 'FAILURE',
                # 'duration': '439300'
                # }
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

                my_stats[job_name][result] += [stats]

    if argv['show']:
        show_report(my_stats)

    if argv['spreadsheet']:
        work = spreadsheet.gen_spreadsheet(my_stats)
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
