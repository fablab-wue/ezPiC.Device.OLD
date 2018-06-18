#!/usr/bin/env python3
"""
TEST
"""
# Meta
__version__ = '0.0.1'
__version_info__ = (0, 0, 1)
__author__ = 'Jochen Krapf et al.'
__license__ = "GNU General Public License (GPL) Version 3"

import sys
#import os, stat, types
import os, os.path

def walktreeX(top = ".", depthfirst = True):
    """Walk the directory tree, starting from top. Credit to Noah Spurrier and Doug Fort."""
    names = os.listdir(top)
    if not depthfirst:
        yield top, names
    for name in names:
        try:
            st = os.lstat(os.path.join(top, name))
        except os.error:
            continue
        if stat.S_ISDIR(st.st_mode):
            for (newtop, children) in walktreeX (os.path.join(top, name), depthfirst):
                yield newtop, children
    if depthfirst:
        yield top, names

#######
def makepath(path):

    """ creates missing directories for the given path and
        returns a normalized absolute version of the path.
    - if the given path already exists in the filesystem
      the filesystem is not modified.
    - otherwise makepath creates directories along the given path
      using the dirname() of the path. You may append
      a '/' to the path if you want it to be a directory path.
    from holger@trillke.net 2002/03/18
    """

    from os import makedirs
    from os.path import normpath,dirname,exists,abspath

    dpath = normpath(dirname(path))
    if not exists(dpath): makedirs(dpath)
    return normpath(abspath(path))

def iterFiles(path_start):
    directories = [path_start]
    while directories:
        directory = directories.pop()
        for name in os.listdir(directory):
            if name.startswith('.') or name.startswith('__'):
                continue
            fullpath = os.path.join(directory,name)
            if os.path.isfile(fullpath):
                yield directory, name
                #print (fullpath)                # That's a file. Do something with it.
            elif os.path.isdir(fullpath):
                directories.append(fullpath) # It's a directory, store it.    

def main():
    srcStartPath = "."

    for srcPath, name in iterFiles(srcStartPath):
        print (srcPath, name)
    


    raise
    import os

    p = os.popen('ls -la')  
    print(p.read())  

#######

if __name__ == '__main__':
    main()

#######

