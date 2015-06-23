#!/usr/bin/env python2

import listparse
reload(listparse)
import os

if __name__ == '__main__':
    #path = '/media/LOCAL_DISK/GAMES/unsortd/r/_1/'
    #dir_ = 'Aki Sora'
    COMMENT = '#'
    with open('paths.txt') as f:
        for path in f.readlines():
            if path[0] != COMMENT:
                print path.rstrip()
                listparse.make_dirs(path.rstrip())
    
