# -*- python -*-

##-------------------##
##---]  GLOBALS  [---##
##-------------------##

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import argparse
import validators

from pathlib           import Path
from validators        import ValidationFailure

from validate.main         import todo               as main_todo

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
def valid_hostname(value: str) -> str:
    """Custom argparse type for domain validation."""

    value = value.strip()
    is_url = validators.domain(value)
    if isinstance(is_url, ValidationFailure):
        msg = 'domain string is invalid: %s' % value
        raise argparse.ArgumentTypeError(msg)

    return value

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
def valid_url(value: str) -> str:
    """Custom argparse type for URL validation."""

    value = value.strip()
    is_url = validators.url(value)
    if isinstance(is_url, ValidationFailure):
        msg = 'URL string is invalid: %s' % value
        raise argparse.ArgumentTypeError(msg)

    return value

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
def valid_spreadsheet(value: str) -> str:
    '''Custom argparse type for output spreadsheet validation.

    :param value: Command line argument value to check (--spread-out) 
    :type  value: str

    :return: Path to a creatable spreadsheet file.
    :rtype:  str
    '''

    value = value.strip()

    if not value.endswith('.ods'):
        path = Path(value).my_file_with_suffix('.ods') # ods, xlsx
        value = path.as_posix()

    if Path(value).exists():
        msg = 'Detected invalid spreadsheet: %s' % (value)
        raise argparse.ArgumentTypeError(msg)

    return value

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
class opt_todo_action(argparse.Action):
    """Display program enhancement list."""

    def __call__(self, parser, args, values, option_string=None):
        main_todo.show_todo()

# [EOF]
