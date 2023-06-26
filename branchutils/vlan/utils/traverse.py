# -*- python -*-
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
"""Common utility function"""

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import os

from pathlib import PurePath

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def traverse(path):
    """Traverse a given directory and display contents."""

    path_str = path.replace('\\', '/')
    path = PurePath(path_str)

    ans = []
    for root, dirs, files in os.walk(path):
        # dirs[:] = [d for d in dirs if d not in exclude]
        for fyl in files:
            ans += [ '/'.join([root, fyl]) ]

    return ans

# EOF
