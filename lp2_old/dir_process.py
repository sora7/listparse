'''
Created on 18.03.2014

@author: alex
'''

import os
import re
import shutil
import HTMLParser

from parsers import pass_year, Dict

WH_DIR = 'wh'
INFO_DIR = 'info'
M_DIR = 'M'
N_DIR = 'N'
G_DIR = 'G'
OST_DIR = 'OST'

################################################################################
# AUTO DIR MAKE
################################################################################

def make_dirs(main_dir):
    def check(s):
        s2 = s
        FORBIDDEN_CHARS = ('?', '"', '`')
        for char in FORBIDDEN_CHARS:
            s2 = s2.replace(char, '')
        return s2

    def check_n_make(fullpath):
        dir_fullpath = check(fullpath)
        return _make_dir(dir_fullpath)

    def _make_dir(fullpath):
        if not os.path.exists(fullpath):
            os.mkdir(fullpath)
            return True
        else:
            # dir exists
            return False

    def prepare(main_dir):
        main = os.path.normpath(main_dir)
        wh_path = os.path.join(main, WH_DIR)

        wh_dirname_ = os.path.join(*wh_path.split(os.path.sep)[-2:])
        if _make_dir(wh_path):
            print 'OK:', wh_dirname_
        else:
            print 'EXISTS:', wh_dirname_
            return None
        
        info_path = os.path.join(wh_path, INFO_DIR)
        _make_dir(info_path)
        
        for item in os.listdir(main):
            if item != 'wh':
                fullpath = os.path.join(main, item)
                shutil.move(fullpath, info_path)

    prepare(main_dir)
    main_dir = os.path.normpath(main_dir)
    info_dir = os.path.join(main_dir, WH_DIR, INFO_DIR)
    titles = process_info_dir(info_dir)
    
    TITLE_PATTERN = '%s'
    YEAR_PATTERN = '(%s)'
    TITLE_YEAR_PATTERN = '%s (%s)'
    for (title, year) in titles:
        if title != None:
            if year != None:
                if YEAR_PATTERN % (year) in title:
                    dir_name = TITLE_PATTERN % (title)
                else:
                    dir_name = TITLE_YEAR_PATTERN % (title, year)
            else:
                dir_name = TITLE_PATTERN % (title)
            main_path = os.path.join(main_dir, dir_name)
            wh_path = os.path.join(main_dir, WH_DIR, dir_name)

            main_path_dirname = os.path.join(*main_path.split(os.path.sep)[-2:])
            if check_n_make(main_path):
                print 'OK:', main_path_dirname
            else:
                print 'EXISTS:', main_path_dirname

            wh_path_dirname = os.path.join(*wh_path.split(os.path.sep)[-3:]) 
            if check_n_make(wh_path):
                print 'OK:', wh_path_dirname
            else:
                print 'EXISTS:', wh_path_dirname
        else:
            # cannot create dir (unknown title)
            pass

def process_info_dir(info_dir):
    titles = []
    
    def is_ignore(filename):
        IGNORE = ('Relations',)
        for item in IGNORE:
            if item in filename:
                return True
        return False
    
    # if os.path.exists(info_dir) and os.path.isdir(info_dir):
    for a_certain_file in os.listdir(info_dir):
        fullpath = os.path.join(info_dir, a_certain_file)
        if os.path.isfile(fullpath) and not is_ignore(a_certain_file):
            # print a_certain_file
            parser = AniDBFileParser()
            with open(fullpath) as f:
                text = ''.join(f.readlines())
                parser.feed(text)
            (title, year) = parser.parse()
            # (title, year) = parse_anidb_file(fullpath)
            titles.append((title, year))
    return titles

################################################################################
# PARSERS
################################################################################

class AniDBFileParser(HTMLParser.HTMLParser):
    __year = None
    __name = None
    __is_header = None
    __is_table = None
    __is_year_row = None
    __is_year_col = None
    __TITLE_REGEXP = re.compile(r'Anime:\s(.+)')
    __YEAR_REGEXP = re.compile(r'(\d{4})')

    def __init__(self):
        self.__year = None
        self.__name = None
        self.__is_header = False
        self.__is_table = False
        self.__is_year_row = False
        self.__is_year_col = False
        
        HTMLParser.HTMLParser.__init__(self)

    def feed(self, data):
        #data = data.replace('</tr><tr', '</tr> <tr')
        HTMLParser.HTMLParser.feed(self, data)
    
    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            attrs = Dict(attrs)
            if attrs['class'] == 'anime':
                self.__is_header = True
        if tag == 'table':
            self.__is_table = True
        if self.__is_table:
            if tag == 'tr':
                attrs = Dict(attrs)
                if attrs['class'] == 'g_odd year':
                    self.__is_year_row = True
            if self.__is_year_row:
                if tag == 'td':
                    attrs = Dict(attrs)
                    if attrs['class'] == 'value':
                        self.__is_year_col = True

    def handle_endtag(self, tag):
        if tag == 'h1':
            if self.__is_header:
                self.__is_header = False
        if tag == 'table':
            self.__is_table = False
        if self.__is_table:
            if tag == 'tr':
                self.__is_year_row = False
            if self.__is_year_row:
                if tag == 'td':
                    self.__is_year_col = False

    def handle_data(self, data):
        if self.__is_header:
            data = str(data)
            if re.search(self.__TITLE_REGEXP, data) is not None:
                title = re.search(self.__TITLE_REGEXP, data).group(1)
                self.__name = title
        if self.__is_table:
            if self.__is_year_row:
                if self.__is_year_col:
                    #print 'YEAR DATA:', data
                    if re.search(self.__YEAR_REGEXP, data) is not None:
                        year = str(re.search(self.__YEAR_REGEXP, data).group(1))
                        self.__year = year

    def parse(self):
        return (self.__name, self.__year)
    
################################################################################
# FUNCTIONS
################################################################################

# unpacking nested lists
# lst = [1,[2,3,[4,5,6]],7,8,9] to
# lst = [1,2,3,4,5,6,7,8,9]
def unpack_list(lst):
    all_items = []
    for item in lst:
        if isinstance(item, list) or isinstance(item, tuple):
            for i in unpack_list(item):
                all_items.append(i)
        else:
            all_items.append(item)
    return all_items

################################################################################
# RES COPY
################################################################################

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
        # print os.path.join(directory, title_dir)
        for item in os.listdir(os.path.join(directory, title_dir)):
            # print item
            if item == WH_DIR:
                input_dir = os.path.join(directory, title_dir, WH_DIR)
                saved_dir = os.path.join(self.stored_dir, title_dir)
                if not os.path.exists(saved_dir):
                    os.mkdir(saved_dir)
                    saved_dir = os.path.join(saved_dir, WH_DIR)
                    shutil.copytree(input_dir, saved_dir)
                    # print 'copy: '
                    # print input_dir
                    # print 'to'
                    # print saved_dir
                    return True
                else:
                    # folder exists
                    pass
        return False

    def process_dir(self, directory, titles_filepath):
        titles = list()
        
        for title_dir in os.listdir(directory):
            # print title_dir
            result = self.search_and_res(directory, title_dir)
            # print result
            if result:
                print title_dir
                titles.append(title_dir)
        # if os.path.exists(titles_filepath):
        with open(titles_filepath, 'w') as f:
            for item in titles:
                f.write('%s %s' % (item, os.linesep))

    def start(self):
        for main_dir in self.main_dirs:
            titles_filename = '%s.txt' % (main_dir.replace(os.path.sep, '_'))
            titles_filepath = os.path.join(self.titles_dir, titles_filename)
            self.process_dir(os.path.abspath(main_dir), titles_filepath)

################################################################################
# FUNCTION
################################################################################

def res_copy(stored_dir, titles_dir):
    stored_dir = 'GAMES/wh/wh_ehd7_f/a/'
    # stored_dir = 'GAMES/wh/wh_ehd7_f/m/'
    titles_dir = 'GAMES/wh/wh_ehd7_f/titles/'
    
    main_dirs = list()
    # main_dirs.append('/media/Index/a')
    # main_dirs.append('/media/Reserve/a')
    # main_dirs.append('/media/temp')
    # main_dirs.append('/media/Index1/a')
    # main_dirs.append('/media/temp1')
    # main_dirs.append('/media/temp2')
    #
    # main_dirs.append('/media/Index/m')
    #
    #

    def search_and_res(directory, title_dir):
        # print os.path.join(directory, title_dir)
        for item in os.listdir(os.path.join(directory, title_dir)):
            # print item
            if item == WH_DIR:
                input_dir = os.path.join(directory, title_dir, WH_DIR)
                saved_dir = os.path.join(stored_dir, title_dir)
                if not os.path.exists(saved_dir):
                    os.mkdir(saved_dir)
                    saved_dir = os.path.join(saved_dir, WH_DIR)
                    shutil.copytree(input_dir, saved_dir)
                    # print 'copy: '
                    # print input_dir
                    # print 'to'
                    # print saved_dir
                    return True
                else:
                    # folder exists
                    pass
        return False
        
    
    def process_dir(directory, titles_filepath):
        titles = list()
        
        for title_dir in os.listdir(directory):
            # print title_dir
            result = search_and_res(directory, title_dir)
            # print result
            if result:
                print title_dir
                titles.append(title_dir)
        # if os.path.exists(titles_filepath):
        with open(titles_filepath, 'w') as f:
            for item in titles:
                f.write('%s %s' % (item, os.linesep))

    for main_dir in main_dirs:
        titles_filename = '%s.txt' % (main_dir.replace(os.path.sep, '_'))
        titles_filepath = os.path.join(titles_dir, titles_filename)
        process_dir(os.path.abspath(main_dir), titles_filepath)

def req_process():
    file_ = '' 
    #make_dirs('/media/2AA92E0025E5B1FF/cop/')
    path = '/media/2AA92E0025E5B1FF/Death Note/'
    import os
    cur_dir = os.path.curdir
    #path = os.path.abspath(os.path.join(os.path.curdir, 'TEST', 'ab'))
    print path
    make_dirs(path)

def test():
    file_ = 'AniDB.net   Anime - Angel Beats!   .htm'
    filepath = path = os.path.abspath(os.path.join(os.path.curdir,
                                                   'TEST',
                                                   'ab',
                                                   file_))
    with open(filepath) as f:
        text = ''.join(f.readlines())
        parser = AniDBFileParser()
        parser.feed(text)
    

if __name__ == '__main__':
    req_process()
    #test()
    pass















