import shutil
import os.path
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="alex"
__date__ ="$18.08.2014 16:03:20$"

import shutil

import whscan

def check_n_make(dir_, n, name=None):
    if name == None:
        name = os.path.basename(dir_)

    if os.path.exists(dir_):
        if os.path.isdir(dir_):
            print '%s EXISTS:' % (name), whscan.take_last(dir_, n)
        else:
            pass
#                 error 
    else:
        os.mkdir(dir_)
        print '%s CREATED' % (name), whscan.take_last(dir_, n)
            
def check_wh_info(path):
    wh_dir, info_dir = whscan.dirs(path)
    
    check_n_make(wh_dir, 2, 'WH')
    check_n_make(info_dir, 3, 'INFO')

def move_info(path):
    wh_dir, info_dir = whscan.dirs(path)

    for item in os.listdir(path):
        if item != whscan.WH_DIRS.WH:
            dst_dir1 = os.path.join(info_dir, item)
            dst_dir2 = os.path.join(wh_dir, item)
            if (not os.path.exists(dst_dir1) and
                not os.path.exists(dst_dir2)
                ):
                item_fullpath = os.path.join(path, item)
                shutil.move(item_fullpath, info_dir)
                print 'MOVE SUCCESSFUL'
            else:
                print 'MOVE FAILED'
                
def make_dirs(path):
    wh_dir, info_dir = whscan.dirs(path)
    titles = whscan.process_info_dir(info_dir)
    dirs = whscan.process_titles(titles)
    for dir_ in dirs:
        dir_ = whscan.check(dir_)
        main_dir = os.path.join(path, dir_)
        wh_dir = os.path.join(path, whscan.WH_DIRS.WH, dir_)
        check_n_make(main_dir, 2, 'MAIN')
        check_n_make(wh_dir, 3, 'WH')

def process_path(path):
    check_wh_info(path)
    move_info(path)
    make_dirs(path)
    
class DirProcess(object):
    
    def __init__(self):
        pass
    
def test():
    path = '/home/alex/prog/workspace/lp/TEST/ab/'
    process_path(path)