# -*- python -*-
## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
"""A module of filesystem traversal methods."""

##-------------------##
##---]  IMPORTS  [---##
##-------------------##
import os

from pathlib import PurePath, Path

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def ferret(path):
    """Traverse with knowledge of a jenkins job directory."""

    path_str = path.replace('\\', '/')
    path = PurePath(path_str)

    # ans  = []
    excl = []
    skip = ['.groovy']
    jobs = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in excl]

        for dx in dirs:
            xyz = '/'.join([root, dx])
            for wanted in ['nextBuildNumber', '.config.xml', 'build', '__found__']:
                nbn  = Path(xyz + '/' + wanted)
            conf = Path(xyz + '/' + 'config.xml')
            print(dx)
            
        for fyl in files:
            xyz = '/'.join([root, fyl])
            obj = Path(xyz)
            suffix = obj.suffix
            # print("** suffix[%s], XYZ: %s" % (suffix, xyz))

            if suffix in skip:
                continue
            elif '/archive/' in xyz:
                continue
            elif suffix in ['.xml']:
                print("FOUND: %s" % obj)

    # return ans

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def history_stats(path):
    """."""

    path_str = path.replace('\\', '/')
    path = PurePath(path_str)

    ans = []
    for root, dirs, files in os.walk(path):
        # dirs[:] = [d for d in dirs if d not in exclude]
        for fyl in files:
            ans += [ '/'.join([root, fyl]) ]

    return ans

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def find_by_name(path, sentinels):
    """Gather a list of filesystem paths that contain a named value from sentinels.

    :param path: Base directory to search.
    :type path: str

    :param sentinels: Names to search for
    :type  sentinels: list[str]

    :return: Filesystem paths sentinel values were detected in.
    :rypte:  list[str]
    """

    path_str = path.replace('\\', '/')
    path = PurePath(path_str)

    ans       = []
    excl      = []
    sentinel  = '__FOUND__'
    sentinels += [sentinel]

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in excl]

        for subdir in dirs:
            for name in sentinels:
                path = '/'.join([root, subdir, name])
                path_obj = Path(path)
                if name == sentinel:
                    found = str(path_obj.parent)
                    ans  += [found]
                    excl += [name] # os.walk(prune=true)
                    continue
                elif not path_obj.exists():
                    break

    return ans

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def find_by_jobdir(path) -> list:
    """Return a list of jenkins job directories.
    
    :param path: Path to a jenkins installation.
    :type  path: str

    :return: Job directory path
    :rtype:  list[str]
    """

    wanted = ['legacyIds', 'permalinks'] # build/permalinks
    ans = [ str(Path(path).parent)
            for path in find_by_name(path, wanted)]

    return ans

## -----------------------------------------------------------------------
## -----------------------------------------------------------------------
def traverse(path:str) -> list:
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
