import os.path
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="alex"
__date__ ="$09.08.2014 16:36:55$"

import os
from parsers.anidb import AniDBParser as TitleParser

class WH_DIRS(object):
    WH = 'wh'
    INFO = 'info'
    A = 'A'
    M = 'M'
    N = 'N'
    G = 'G'
    OST = 'OST'

def check(text):
    FORBIDDEN_CHARS = ('?', '"', '`')
    for char in FORBIDDEN_CHARS:
        text = text.replace(char, '')
    return text

def take_last(path, n):
    if n == 0:
        return ''
    else:
        sep = '' if n == 1 else os.path.sep
        head, tail = os.path.split(path)
        return take_last(head, n-1) + sep + tail    

def dirs(path):
    wh_dir = os.path.join(path, WH_DIRS.WH)
    info_dir = os.path.join(path, WH_DIRS.WH, WH_DIRS.INFO)
    return (wh_dir, info_dir)

def process_titles(titles):
    dirs = []
    
    TITLE_PATTERN = '%s'
    YEAR_PATTERN = '%s'
    TITLE_YEAR_PATTERN = '%s (%s)'
    
    for title, year in titles:
        if title != None:
            if year != None:
                if YEAR_PATTERN % (year) in title:
                    dir_name = TITLE_PATTERN % (title)
                else:
                    dir_name = TITLE_YEAR_PATTERN % (title, year)
            else:
                dir_name = TITLE_PATTERN % (title)
            dirs.append(dir_name)
        else:
            # cannot create dir (unknown title)
            pass
    return dirs

def process_info_dir(info_dir):
    join = os.path.join
    ls = os.listdir
    isfile = os.path.isfile

    IGNORE_NAMES = ('Relations',)

    ignore_files = lambda name: bool(filter(lambda ig: ig in name, IGNORE_NAMES))
    not_ignore = filter(lambda item : not ignore_files(item), ls(info_dir))
    dir_items = map(lambda x: join(info_dir, x), not_ignore)
    info_files = filter(lambda item : isfile(item), dir_items)

    titles = []
    for info_file in info_files:
        parser = TitleParser()
        (title, year) = parser.title(info_file)
        titles.append((title, year))
    return titles

def test():
    path = '/home/alex/prog/workspace/'
    path = os.path.normpath(path)
    print path
    print take_last(path, 1)
    print take_last(path, 2)
    print take_last(path, 3)