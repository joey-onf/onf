# -*- python -*-

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import sys
import argparse
import pprint

# import iptools      # IP Addresse
from IPy import IP  # IPv4 & IPv6
import datetime

from vlan.main   import utils      as main_utils
from vlan.main   import todo       as main_todo

# -----------------------------------------------------------------------
# datetime: validation
# argparse: error handling
# -----------------------------------------------------------------------
def valid_shift_time_type(arg_shift_time_str: str) -> datetime:
    """Custom argparse type for user shift time values given from the command line"""
    try:
        return datetime.strptime(arg_shift_time_str, "%H:%M")
    except ValueError:
        msg = "Given shift time ({}) not valid! Expected format, 'HH:MM'!".format(arg_shift_time_str)
        raise argparse.ArgumentTypeError(msg)
## -----------------------------------------------------------------------
## Intent: Validate --netmask xx.xx.xx/ddd value passed
## -----------------------------------------------------------------------
## https://medium.com/@zackbunch/how-to-create-custom-argparse-types-in-python-608c17d1f94a
## -----------------------------------------------------------------------
def valid_netmask_2(netmask: str) -> str:
    """Custom argparse type for netmask string validation of command line args."""

    # ---------------------------------------
    # https://pypi.org/project/IPy/
    # https://github.com/autocracy/python-ipy
    # IP().len() -vs- len(IP) for comparison
    # --------------------------------------- 
    try:
        IP(netmask)

    except ValueError:
        err = "Detected invalid argument: --netmask %s" % netmask
        raise argparse.ArgumentTypeError(err)

    return netmask

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def get_argv(type_dict=None):
    """Retrieve parsed command line switches.

    :param type_dict: Type of parsed switch storage to return.
    :param type_dict: bool, conditional

    :return: Parsed command line argument storage
    :rtype : [namespace|dict] (default: namespace)
    """

    global ARGV

    ans = namespace if type_dict is None else ARGV
    return ans

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
class valid_netmask(argparse.Action):
    """Verify incoming switch value is a valid netmask."""

    def __call__(self, parser, args, value, option_string=None):

        iam = main_utils.iam()
        pprint.pprint({
            'iam'  : iam,
            'args-raw' : args,
            'args-var' : vars(args),
        })
        sys.exit(1)
        
        attrs = vars(args)

        if self.dest in attrs and attrs[self.dest]:
            cached = attrs[self.dest]
            if value.lower() != cached.lower():
                parser.error("Detected multiple %s values: %s, %s" \
                             % (option_string, cached, value))
        else:
            setattr(args, self.dest, value)

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
class unique_scalar(argparse.Action):
    """Verify incoming switch value is consistent.

    Values may be passed in by a combination of args.
        o --application
        o --tagname

    This method will detect when variant values are passed in.
    """
    def __call__(self, parser, args, value, option_string=None):

        attrs = vars(args)

        if self.dest in attrs and attrs[self.dest]:
            cached = attrs[self.dest]
            if value.lower() != cached.lower():
                parser.error("Detected multiple %s values: %s, %s" \
                             % (option_string, cached, value))
        else:
            setattr(args, self.dest, value)

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
class opt_help_action(argparse.Action):
    """Display program help text."""

    def __call__(self, parser, args, values, option_string=None):
        help.show_help()

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
class opt_tag_action(argparse.Action):
    """Digest a tagname argument.

    1) Validate tagname syntax.
    2) Extract and append additional command line arguments.
         o application
         o battree
         o component
    """

    def __call__(self, parser, args, tagname, option_string=None):

        ## -----------------------
        ## Validate tagname syntax
        ## -----------------------
        try:
            obj  = TagName.TagName(tagname)

            if hasattr(obj, 'application'):
                sys.argv.extend(['--application', obj.application])
            if hasattr(obj, 'tree'):
                sys.argv.extend(['--tree',     obj.tree])
            if hasattr(obj, 'changeset'):
                sys.argv.extend(['--changeset',   obj.changeset])

        except Exception as err:
            print("%s\n" % err)
            parser.error("--tagname is invalid %s" % tagname)

        ## -----------------------------------------------
        ## Accumulate tagname args, we may need them later
        ## -----------------------------------------------
        tagnames = [tagname]
        cached   = vars(args)
        if 'tagname' in cached and cached['tagname']:
            tagnames.extend(cached['tagname'])

        setattr(args, self.dest, tagnames)

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
class opt_todo_action(argparse.Action):
    """Display program enhancement list."""

    def __call__(self, parser, args, values, option_string=None):
        main_todo.show_todo()

# [EOF]
