#!/usr/bin/env python2
##  PYTHON 2!!!!!!!!!!!!!!!!!!!

import os
import sys
import re
import shutil

MODULES_DIR = 'modules'

M_DIR = 'M'
N_DIR = 'N'
G_DIR = 'G'
OST_DIR = 'OST'
WH_DIR = 'wh'
INFO_DIR = 'info'

######################################################################
# RES COPY
######################################################################

class ResCopy():
    stored_dir = None
    titles_dir = None
    main_dirs = None
    
    def __init__(self):
        self.stored_dir = ''
        self.titles_dir = ''
        self.main_dirs = []

    def set_dirs(self, store, titles):
        self.stored_dir = store
        self.titles_dir = titles
    
    def add(self, dir_):
        self.main_dirs.append(dir_)
    
    def search_and_res(self, directory, title_dir):
        #print os.path.join(directory, title_dir)
        for item in os.listdir(os.path.join(directory, title_dir)):
            #print item
            if item == WH_DIR:
                input_dir = os.path.join(directory, title_dir, WH_DIR)
                saved_dir = os.path.join(self.stored_dir, title_dir)
                if not os.path.exists(saved_dir):
                    os.mkdir(saved_dir)
                    saved_dir = os.path.join(saved_dir, WH_DIR)
                    shutil.copytree(input_dir, saved_dir)
                    #print 'copy: '
                    #print input_dir
                    #print 'to'
                    #print saved_dir
                    return True
                else:
                    # folder exists
                    pass
        return False

    def process_dir(self, directory, titles_filepath):
        titles = list()
        
        for title_dir in os.listdir(directory):
            #print title_dir
            result = self.search_and_res(directory, title_dir)
            #print result
            if result:
                print title_dir
                titles.append(title_dir)
        #if os.path.exists(titles_filepath):
        with open(titles_filepath, 'w') as f:
            for item in titles:
                f.write('%s %s'%(item, os.linesep))

    def start(self):
        for main_dir in self.main_dirs:
            titles_filename = '%s.txt'%(main_dir.replace(os.path.sep, '_'))
            titles_filepath = os.path.join(self.titles_dir, titles_filename)
            self.process_dir(os.path.abspath(main_dir), titles_filepath)
        
def res_copy_script():
    main_save = '/media/Локальный диск/GAMES/wh/wh_ehd7_f/'
    titles = os.path.join(main_save, 'titles')
    
    def a():
        save = os.path.join(main_save, 'a')
        res = ResCopy()
        res.set_dirs(save, titles)
        #res.add('/media/Локальный диск/GAMES/unsortd/_/')
        
        #res.add('/media/Index/a')
        #res.add('/media/Reserve/a')
        #res.add('/media/temp/Other')
        #
        res.add('/media/Index_1/a')
        res.add('/media/Index_2/a')
        res.add('/media/temp_1/_')
        res.add('/media/temp_2/_')
        res.start()
        
    def m():        
        save = os.path.join(main_save, 'm')
        res = ResCopy()
        res.set_dirs(save, titles)
        res.add('/media/Index/m')
        res.start()

    a()
    #m()

# FUNCTION ###########################################################

def res_copy(stored_dir, titles_dir):
    stored_dir = '/media/Локальный диск/GAMES/wh/wh_ehd7_f/a/'
    #stored_dir = '/media/Локальный диск/GAMES/wh/wh_ehd7_f/m/'
    titles_dir = '/media/Локальный диск/GAMES/wh/wh_ehd7_f/titles/'
    
    main_dirs = list()
    #main_dirs.append('/media/Index/a')
    #main_dirs.append('/media/Reserve/a')
    #main_dirs.append('/media/temp')
    #main_dirs.append('/media/Index1/a')
    #main_dirs.append('/media/temp1')
    #main_dirs.append('/media/temp2')
    #
    #main_dirs.append('/media/Index/m')
    #
    main_dirs.append('/media/Локальный диск/GAMES/unsortd/_/')
    #

    def search_and_res(directory, title_dir):
        #print os.path.join(directory, title_dir)
        for item in os.listdir(os.path.join(directory, title_dir)):
            #print item
            if item == WH_DIR:
                input_dir = os.path.join(directory, title_dir, WH_DIR)
                saved_dir = os.path.join(stored_dir, title_dir)
                if not os.path.exists(saved_dir):
                    os.mkdir(saved_dir)
                    saved_dir = os.path.join(saved_dir, WH_DIR)
                    shutil.copytree(input_dir, saved_dir)
                    #print 'copy: '
                    #print input_dir
                    #print 'to'
                    #print saved_dir
                    return True
                else:
                    # folder exists
                    pass
        return False
        
    
    def process_dir(directory, titles_filepath):
        titles = list()
        
        for title_dir in os.listdir(directory):
            #print title_dir
            result = search_and_res(directory, title_dir)
            #print result
            if result:
                print title_dir
                titles.append(title_dir)
        #if os.path.exists(titles_filepath):
        with open(titles_filepath, 'w') as f:
            for item in titles:
                f.write('%s %s'%(item, os.linesep))

    for main_dir in main_dirs:
        titles_filename = '%s.txt'%(main_dir.replace(os.path.sep, '_'))
        titles_filepath = os.path.join(titles_dir, titles_filename)
        process_dir(os.path.abspath(main_dir), titles_filepath)

######################################################################                
    
def import_modules():
    modules_path = os.path.join(os.path.curdir, MODULES_DIR)
    if not (modules_path in sys.path):
        sys.path.append(modules_path)

if __name__ == '__main__':
    import_modules()
    res_copy_script()












    
