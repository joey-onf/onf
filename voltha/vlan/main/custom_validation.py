from datetime import datetime
import argparse

# datetime: validation
# argparse: error handling
def valid_shift_time_type(arg_shift_time_str: str) -> datetime:
    """Custom argparse type for user shift time values given from the command line"""
    try:
        return datetime.strptime(arg_shift_time_str, "%H:%M")
    except ValueError:
        msg = "Given shift time ({}) not valid! Expected format, 'HH:MM'!".format(arg_shift_time_str)
        raise argparse.ArgumentTypeError(msg)

# [EOF]
