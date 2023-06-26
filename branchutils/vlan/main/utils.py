# -*- python -*-
## -----------------------------------------------------------------------
## Intent: This module contains general helper methods
## -----------------------------------------------------------------------

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import contextlib
import sys
import os
import pprint

from pathlib import Path

import tempfile
import shutil             # rmtree

## ---------------------------------------------------------------------------
## ---------------------------------------------------------------------------
def iam():
    """Return name of a called method."""

    func_name = sys._getframe(1).f_code.co_name # pylint: disable=protected-access
    iam       = "%s::%s" % (__name__, func_name)
    return iam

## ---------------------------------------------------------------------------
## ---------------------------------------------------------------------------
def banner(label, *args, pre=None, post=None) -> None:
    """Format output with delimiters for visibility.

    :param pre: Display leading whitespace.
    :type  pre: bool

    :param post: Display leading whitespace.
    :type  post: bool
    """

    if pre:
        print('')

    hyphens = '-' * 71
    print(" ** %s" % hyphens)
    print(" ** %s" % label)

    for arg in args:
        if isinstance(arg, dict):
            pprint.pprint(arg)
        elif isinstance(arg, list):
            todo = arg
            # todo = list_utils.flatten(arg)
            for line in todo:
                print(" ** %s" % line)
        else:
            print(" ** %s" % arg)

    print(" ** %s" % hyphens)

    if post:
        print('')

## -----------------------------------------------------------------------
## Intent: Display a message then exit with non-zero status.
##   This method cannot be intercepted by try/except
## -----------------------------------------------------------------------
def error(msg, exit_with=None, fatal=None):
    """Display a message then exit with non-zero status.

    :param msg: Error mesage to display.
    :type  msg: string

    :param exit_with: Shell exit status.
    :type  exit_with: int, optional (default=2)

    :param fatal: When true raise an exception.
    :type  fatal: bool (default=False)

    """

    if exit_with is None:
        exit_with = 2

    if fatal is None:
        fatal = false

    if msg:
        if fatal:
            raise Exception("ERROR: %s" % msg)
        else:
            print("")
            print("ERROR: %s" % msg)

    sys.exit(exit_with)

## -----------------------------------------------------------------------
## Intent: Helper method, format an error string then thrown an exception.
##   multi-line strings thrown within an exception are ugly, lines become
##   interspersed with callstack.  Display error text with log delimiters
##   then throw a simple summary message
## -----------------------------------------------------------------------
##  Given:
##    string  - summary to throw exception on
##    array   - strings to display before error is thrown
## -----------------------------------------------------------------------
## Usage:
##        msg = "Detected upload failure"
##        detail = pprint.pformat({
##            'iam' : main_utils.iam(),
##            'ERROR'     : msg,
##            'EXCEPTION' : err,
##            'method-args' : {
##                'src'  : src,
##                'argv' : argv,
##                'tag'  : tag,
##            },
##        }, indent=4)
##        main_utils.my_except(msg, detail)
## -----------------------------------------------------------------------
def my_except(summary, *args):

    me = iam() # iam = iam() reports use before definition in this module
    msg = "ERROR: %s" % summary
    pp = pprint.PrettyPrinter(indent=4, compact=False)

    detail = pp.pformat({
        'iam'     : iam(),
        'args'    : args,
    })

    print("""
===========================================================================
 ** %s
 ** %s
===========================================================================
""" % (msg, detail))

    raise Exception(summary)

## -----------------------------------------------------------------------
## Intent: Emulate pushd/popd/chdir directory stack
## Usage:
##    with utils.pushd('/var/tmp'):
##        print(" ** getcwd[1] %s" % os.getcwd())
## -----------------------------------------------------------------------
@contextlib.contextmanager
def pushd(new_dir=None, debug=None, tempdir=None, systemp=None):
    """Emulate pushd/popd/chdir directory stack.

    :param debug: Enable debug mode
    :type  debug: bool

    :param new_dir: Chdir to this named directory
    :type  new_dir: string

    :param tempdir: Create a temporary dirctory as source for pushd.
    :type  tempdir: bool

    :param systemp: Shorten path: create in system@tmp rather than jenkins@tmp
    :type  systemp: bool

    :return: yield back to caller

    Usage:
    with main_utils.pushd('/home'):
        print(" ** cd %s" % os.cwd())

    with main_utils.pushd(tempdir=True):
        print(" ** tempdir is: %s" % os.cwd())
    """

    if debug is None:
        debug = False

    old_dir = Path('.').resolve().as_posix()

    if debug:
        print(" ** pushd %s (pwd=%s)" % (new_dir, old_dir))

    temp_dir = None # rm tempdir when storage goes out of scope

    if tempdir:
        # Difficult calling temporary_directory() generator here
        # Separate path handling to prevent mishaps.
        temp_dir = tempfile.mkdtemp()
        new_dir  = temp_dir

    elif systemp:
        root = tempfile.gettempdir()
        temp_dir = tempfile.mkdtemp(dir=root)
        new_dir  = temp_dir

    elif new_dir is None:
        raise ValueError("ERROR: new_dir is required" % new_dir)

    elif not isinstance(new_dir, str):
        raise ValueError("ERROR: Invalid path argument detected (new_dir=[%s])" % new_dir)

    os.chdir(new_dir)

    if debug:
        print(" ** %s: chdir(%s) from %s" % (iam(), new_dir, old_dir))

    try:
        yield
    finally:
        if debug:
            print(" ** popd %s" % new_dir)
        os.chdir(old_dir)
        if tempdir:
            shutil.rmtree(temp_dir)

    return

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
@contextlib.contextmanager
def temporary_directory():
    """Create a transient temporary directory.

    Usage:
    with temporary_directory() as temp_dir:
        ... do stuff with temp_dir ...
    """

    # suffix=None, prefix=none, dir=None
    d = tempfile.mkdtemp()
    try:
        yield d
    finally:
        shutil.rmtree(d)

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def todo():
    """Display future enhancement list."""

    print("""
[TODO: %s]
  o Support with pushd('/foo/bar', tempdir=True)
      - Call would create a transient temp directory while context exists.
      - export tmp={tempdir} or TMP={tempdir} as needed.
      - Caller would have access to a dedicated temp directory while
        context for chdir(/foo/bar) exists.
""" % iam())

    return

# EOF
