#!/usr/bin/env python2

import os

def cl(path):
    for item in os.listdir(path):
        item_full = os.path.join(path, item)
        if os.path.isdir(item_full):
#           print 'DIR: ', item_full
           cl(item_full)
        if os.path.isfile(item_full):
#           print 'FILE: ', item_full
            if os.path.basename(item_full).endswith('pyc'):
               print 'DELETED', os.path.basename(item_full)
               os.remove(item_full)

if __name__ == '__main__':
    dir_ = 'src/listparse'
    path = os.path.join(os.path.abspath(os.curdir), dir_)
    cl(path)