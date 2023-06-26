#!/usr/bin/env python
'''.'''

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import sys
from pathlib import Path

if True: # Set searchpath early
    pgm = sys.argv[0]
    pgm_path = Path(pgm).resolve()
    anchor = Path(pgm_path).parent.parent.as_posix()
    sys.path.insert(0, anchor)

import pprint
from pathlib           import Path

from validate.main        import utils           as main_utils
from validate.main        import argparse        as main_getopt

from validate.struct      import data_structure  as ds

## ---------------------------------------------------------------------------
## ---------------------------------------------------------------------------
def process():
    '''.'''

    argv  = main_getopt.get_argv()

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def init(argv_raw) -> None:
    '''Prep for a script run.'''

    ## Move to class validate/main/utils.py
    main_getopt.getopts(argv_raw)    
    argv  = main_getopt.get_argv()

    return
    
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def main(argv_raw):
    '''.'''

    init(argv_raw)
    argv  = main_getopt.get_argv()
    if argv['verbose']:
        pprint.pprint(argv)
            
    # process()

##----------------##
##---]  MAIN  [---##
##----------------##
if __name__ == "__main__":
    main(sys.argv[1:]) # NOSONAR

# [EOF]
