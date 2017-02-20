#!/usr/bin/env python2
##  PYTHON 2!!!!!!!!!!!!!!!!!!!

# -*- coding: utf-8 -*-

#==============================================================================#
import os
import sys
import re
import StringIO
import shutil
# import tkFileDialog
# import ttk

import HTMLParser
import re
import base64

import Tkinter
#------------------------------------------------------------------------------#
MODULES_DIR = 'modules'

#------------------------------------------------------------------------------#
try:
    import bs4
except ImportError:
    modules_path = os.path.join(os.path.curdir, MODULES_DIR)
    if not (modules_path in sys.path):
        sys.path.append(modules_path)
    import bs4
#==============================================================================#

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

def test0():
    file_ = 'AniDB.net   Anime - Angel Beats!   .htm'
    filepath = path = os.path.abspath(os.path.join(os.path.curdir,
                                                   'TEST',
                                                   'ab',
                                                   file_))
    with open(filepath) as f:
        text = ''.join(f.readlines())
        parser = AniDBFileParser()
        parser.feed(text)
    
################################################################################
# LIST PARSERS
################################################################################

class AniTitle(object):
    __ani_id = None
    __ani_name = None
    __ani_link = None
    __char_id = None
    __char_name = None
    __char_link = None
    __type = None
#     int
    __eps = None
    __s_eps = None
#     str
    __year = None
    __year_start = None
    __year_end = None
    __date_start = None
    __date_end = None
#     bool
    __completed = None
    # #
    __empty = None

    def __init__(self):
        self.__ani_id = None
        self.__ani_name = None
        self.__ani_link = None
        self.__char_id = None
        self.__char_name = None
        self.__char_link = None
        self.__type = None
                
        self.__eps = None
        self.__s_eps = None
        
        self.__year = None
        self.__year_start = None
        self.__year_end = None
        self.__date_start = None
        self.__date_end = None
        
        self.__completed = False
        self.__empty = True
        
    @property
    def ani_id(self):
        return self.__ani_id
    
    @ani_id.setter
    def ani_id(self, value):
        self.__ani_id = value
        self.__empty = False
        
    @property
    def ani_name(self):
        return self.__ani_name
    
    @ani_name.setter
    def ani_name(self, value):
        self.__ani_name = value
        self.__empty = False   

    @property
    def ani_link(self):
        return self.__ani_link
    
    @ani_link.setter
    def ani_link(self, value):
        self.__ani_link = value
        self.__empty = False        

    @property
    def char_id(self):
        return self.__char_id
    
    @char_id.setter
    def char_id(self, value):
        self.__char_id = value
        self.__empty = False
        
    @property
    def char_name(self):
        return self.__char_name
    
    @char_name.setter
    def char_name(self, value):
        self.__char_name = value
        self.__empty = False   

    @property
    def char_link(self):
        return self.__char_link
    
    @char_link.setter
    def char_link(self, value):
        self.__char_link = value
        self.__empty = False
        
    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, value):
        self.__type = value
        self.__empty = False

    @property
    def eps(self):
        return self.__eps
    
    @eps.setter
    def eps(self, value):
        self.__eps = value
        self.__empty = False
        
    @property
    def s_eps(self):
        return self.__s_eps
    
    @s_eps.setter
    def s_eps(self, value):
        self.__s_eps = value
        self.__empty = False

    @property
    def year(self):
        return self.__year
    
    @year.setter
    def year(self, value):
        self.__year = value
        self.__empty = False
    
    @property
    def year_start(self):
        return self.__year_start
    
    @year_start.setter
    def year_start(self, value):
        self.__year_start = value
        self.__empty = False
    
    @property
    def year_end(self):
        return self.__year_end
    
    @year_end.setter
    def year_end(self, value):
        self.__year_end = value
        self.__empty = False
        
    @property
    def date_start(self):
        return self.__date_start
    
    @date_start.setter
    def date_start(self, value):
        self.__date_start = value
        self.__empty = False
    
    @property
    def date_end(self):
        return self.__date_end
    
    @date_end.setter
    def date_end(self, value):
        self.__date_end = value
        self.__empty = False
        
    @property
    def completed(self):
        return self.__completed
    
    @completed.setter
    def completed(self, value):
        self.__completed = value
        self.__empty = False
        
    @property
    def empty(self):
        return self.__empty

class keys(object):
    ANI_NAME = 'ani_name'
    ANI_ID = 'ani_id'
    ANI_LINK = 'ani_link'
    CHAR_NAME = 'char_name'
    CHAR_ID = 'char_id'
    CHAR_LINK = 'char_link'
    TYPE = 'type'
    EPS = 'eps'
    S_EPS = 's_eps'
    YEAR = 'year'
    YEAR_START = 'year_start'
    YEAR_FINISH = 'year_finish'
    DATE_START = 'date_start'
    DATE_FINISH = 'date_finish'
    COMPLETED = 'completed'
    # list keys
    LIST_NAME = 'list_name'
    LIST_TYPE = 'list_type'
    LIST_PATH = 'list_path'
    # filetypes
    FTYPE_PERSON = 'person'
    FTYPE_COMPANY = 'company'
    FTYPE_MYLIST = 'mylist'

def pass_year(title, date):
    # '1995 - 1996'
    # 'XXXX - XXXX'
    date_regexp = re.compile(r'\s{0,1}-{0,1}\s{0,1}(.{4})\s{0,1}-{0,1}\s{0,1}')
    date_lst = re.findall(date_regexp, str(date))
    
    if len(date_lst) == 1:
        finish = date_lst[0]
    elif len(date_lst) == 2:
        finish = date_lst[1]
    else:
        raise ValueError('input data error')
    year, start = date_lst[0], date_lst[0]
    
    title.year = year
    title.year_start = start
    title.year_end = finish
    
    return (year, start, finish)

def conv(inp_str):
    try:
        return str(inp_str)
    except UnicodeEncodeError:
        try:
            return ''.join(chr(char) for char in inp_str)
        except TypeError:
            # return inp_str
            return None

class Bool(object):
    '''
    Mutable boolean class
    '''
    __value = None

    def __init__(self, val=False):
        self.__value = bool(val)
        self.__bool__ = self.__nonzero__

    def __nonzero__(self):
        return self.__value

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self.__value)
    '''
    instead of assignment '=' we use addition '+' 
    '''
    def __add__(self, other):
        self.__value = bool(other)

class Dict():
    '''
    dictionary class who return None if has no key
    (do not raise exceptions)
    '''
    __store = None
    
    def __init__(self, input_lst):
        self.__store = dict()
        
        for (key, value) in input_lst:
            self.__store[conv(key)] = conv(value)
    
    def __getitem__(self, key):
        if self.__store.has_key(key):
            return self.__store[key]
        else:
            return None

class ListType(object):
    @property
    def UNKNOWN(self):
        return 0
    
    @property
    def PERSON(self):
        return 1
    
    @property 
    def COMPANY(self):
        return 2
    
    @property 
    def MYLIST(self):
        return 3

listtype = ListType()

class AniList(object):
    __type = None
    __name = None
    __path = None
    __list = None
    
    def __init__(self):
        self.__type = listtype.UNKNOWN
        self.__name = None
        self.__path = None
        self.__list = []
    
    @property
    def type(self):
        return self.__type
    
    @type.setter
    def type(self, value):
        self.__type = value

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def path(self):
        return self.__path
    
    @path.setter
    def path(self, value):
        self.__path = value
    
    @property    
    def lst(self):
        return self.__list 

    @lst.setter
    def lst(self, value):
        self.__lst = value

class StopPleaseException(Exception):
    def __init__(self):
        pass
#     
#     def __init__(self, message, Errors):
#         Exception.__init__(self, message)
#         self.Errors = Errors

class PersonParser(HTMLParser.HTMLParser):
    is_table = False
    is_row = False
    is_col = False

    CHAR_LINK = 'http://anidb.net/perl-bin/animedb.pl\?show=character&charid='
    CHAR_LINK_PATTERN = re.compile(CHAR_LINK + '(\d+)')
    ANI_LINK = 'http://anidb.net/perl-bin/animedb.pl\?show=anime&aid='
    ANI_LINK_PATTERN = re.compile(ANI_LINK + '(\d+)')

    titles = []
    
    charid_zero = False

    is_char = False
    is_char_link = False
    is_ani = False
    is_ani_link = False
    
    is_type = False
    is_eps = False
    is_year = False

    __char_link = ''
    __char_id = ''
    __char_name = ''
    __ani_link = ''
    __ani_id = ''
    __ani_name = ''
    
    __type = ''
    __year = ''
    __eps = ''
    
    def is_data_empty(self):
        _len = 0
        for item in (self.__ani_id, self.__ani_link, self.__ani_name,
                     self.__char_name, self.__type, self.__year, self.__eps):
            if len(item) == 0:
                return True
        return False
    
    def __init__(self):
        self.titles = []
        HTMLParser.HTMLParser.__init__(self)
    
    def feed(self, data):
        '''
        stupid HTMLParser understand the folowing:
        <tr>spam spam</tr><tr>more spam</tr>
        as ONE row
        next code works fine:
        <tr>spam spam</tr> <tr>more spam</tr>
                          ^
                        fucking whitespace
        html syntax fix (whitespaces beetween <tr> tags)
        '''
#         HTMLParser.HTMLParser.reset(self)
        self.reset()
        data = data.replace('</tr><tr', '</tr> <tr')
        HTMLParser.HTMLParser.feed(self, data)
    
    def handle_starttag(self, tag, attrs):
        attrs = Dict(attrs)
        
        if tag == 'table':
            if (attrs['id'] == 'characterlist' and
                attrs['class'] == 'characterlist'):
                self.is_table = True
                
        if self.is_table:
            if tag == 'tr':
                self.is_row = True
                if attrs['id'] == 'charid_0':
                    self.charid_zero = True
                    
        if self.is_row:
            if tag == 'td':
                self.is_col = True
                
        if self.is_col:
            if attrs['class'] == 'name':
                if attrs['rowspan'] != None:
                    self.is_char = True
                else:
                    self.is_ani = True
            if attrs['class'] == 'type':
                self.is_type = True
            if attrs['class'] == 'eps':
                self.is_eps = True
            if attrs['class'] == 'year':
                self.is_year = True

        if self.is_char:
            if tag == 'a':
                link = attrs['href']
                # print link
                if self.CHAR_LINK_PATTERN.match(link):
                    self.__char_id = self.CHAR_LINK_PATTERN.findall(link)[0]
                    self.__char_link = link
                    self.is_char_link = True

        if self.is_ani:
            if tag == 'a':
                link = attrs['href']
                if self.ANI_LINK_PATTERN.match(link):
                    self.__ani_id = self.ANI_LINK_PATTERN.findall(link)[0]
                    self.__ani_link = link
                    self.is_ani_link = True
                    
    def handle_endtag(self, tag):
        if tag == 'table':
            self.is_table = False
        if self.is_table:
            if tag == 'tr':
                self.is_row = False
                        
        if self.is_row:
            if tag == 'td':
                self.is_col = False
                
        if self.is_char_link:
            if tag == 'a':
                self.is_char_link = False

        if self.is_ani_link:
            if tag == 'a':
#                 self.__ani_id = ''
                self.is_ani_link = False
            
    def handle_data(self, data):
        if self.is_table:
            if self.is_row:
#                 print 'row'
                if self.is_col:
                    if self.is_char:
                        if self.charid_zero:
                            self.__char_name = data.strip()
                            self.charid_zero = False
                            self.is_char = False
                        if self.is_char_link:
                            self.__char_name = data
                            self.is_char = False
                    if self.is_ani:
                        if self.is_ani_link:
                            self.__ani_name = data
                            self.is_ani = False
                    if self.is_type:
                        self.__type = str(data)
                        self.is_type = False
                    if self.is_eps:
                        self.__eps = str(data)
                        self.is_eps = False
                    if self.is_year:
                        self.__year = str(data)
                        self.is_year = False
            else:
#                 row ends
                if not self.is_data_empty():
                    title = AniTitle()
                    title.ani_id = self.__ani_id
                    title.ani_name = self.__ani_name
                    title.ani_link = self.__ani_link
                    title.char_id = self.__char_id
                    title.char_name = self.__char_name
                    title.char_link = self.__char_link                
                    title.type = self.__type
                    title.eps = self.__eps
                    pass_year(title, self.__year)
                    self.titles.append(title)    
    @property
    def titles(self):
        return self.titles

class CompanyParser(HTMLParser.HTMLParser):
    is_table = False
    is_row = False
    is_col = False    
    
    is_name = None
    is_type = None
    is_eps = None
    is_year = None
    is_credit = None
    
    ani_id = None
    ani_name = None
    ani_link = None
    type = None
    eps = None
    year = None
    credit = None
#     list
    __animes = None

    def __init__(self):
        self.__animes = []
        HTMLParser.HTMLParser.__init__(self)

    def feed(self, data):
        '''
        stupid HTMLParser understand the folowing:
        <tr>spam spam</tr><tr>more spam</tr>
        as ONE row
        next code works fine:
        <tr>spam spam</tr> <tr>more spam</tr>
                          ^
                        fucking whitespace
        html syntax fix (whitespaces beetween <tr> tags)
        '''
        HTMLParser.HTMLParser.reset(self)
        self.reset()
        data = data.replace('</tr><tr', '</tr> <tr')
#         data = data.replace('</td><td', '</td> <td')
        HTMLParser.HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        attrs = Dict(attrs)
        
        if tag == 'table':
            if (attrs['id'] == 'stafflist' and
                attrs['class'] == 'stafflist'
                ):
                self.is_table = True

        if self.is_table:
            if tag == 'tr':
                self.is_row = True
                
        if self.is_row:
            if tag == 'td':
                self.is_col = True
                
        if self.is_col:
            if attrs['class'] == 'name':
                self.is_name = True
            if self.is_name:
                if tag == 'a':
                    self.ani_link = attrs['href']
                    print self.ani_link
#http://anidb.net/perl-bin/animedb.pl?show=anime&aid=15                    
#                 pass_link()              
                    ###############
                    ###############
                    ###############
                    ###############
                    ###############
                    ###############
                    ###############
                    ###############
                    ###############
                    ###############
                    ###############
                    ###############
                
            if attrs['class'] == 'type':
                self.is_type = True

            if attrs['class'] == 'eps':
                self.is_eps = True
                
            if attrs['class'] == 'year':
                self.is_year = True

            if attrs['class'] == 'credit':
                self.is_credit = True

    def handle_endtag(self, tag):
        if tag == 'table':
            self.is_table = False
            
        if self.is_table:
            if tag == 'tr':
                self.is_row = False
                
        if self.is_row:
            if tag == 'td':
                self.is_col = False
                
        if self.is_col:
            if tag == 'td':
                self.is_col = False
                
        if self.is_name:
            if tag == 'td':
                self.is_name = False
                
        if self.is_type:
            if tag == 'td':
                self.is_type = False
                
        if self.is_eps:
            if tag == 'td':
                self.is_eps = False
        
        if self.is_year:
            if tag == 'td':
                self.is_year = False
                
        if self.is_credit:
            if tag == 'td':
                self.is_credit = False
                        
    def handle_data(self, data):
        if self.is_table:
            if self.is_row:
                if self.is_col:
                    if self.is_name:
                        self.ani_name = data
                    if self.is_type:
                        self.type = data
                    if self.is_eps:
                        self.eps = data
#                         print 'eps:', data
                    if self.is_year:
                        self.year = data
#                         print 'year:', data
                    if self.is_credit:
                        self.credit = data
            else:
                title = AniTitle()
                title.ani_name = self.ani_name
                title.ani_id = self.ani_id
                #print self.ani_id
                title.ani_link = self.ani_link
                pass_year(title, str(self.year))
                
                title.type = self.type
                self.__animes.append(title)
    
    @property
    def titles(self):
        return self.__animes

class MALParser(HTMLParser.HTMLParser):
    
    def handle_starttag(self, tag, data):
        pass
    
    def handle_endtag(self, tag):
        pass
    
    def handle_data(self, data):
        pass

class MylistParser(HTMLParser.HTMLParser):
    is_animes = False
    is_ani = False
    is_titles = False
    is_title = False    
    
    # TODO: rewrite using self.ani_id self.type and so on 
    
    __animes = []
    ani = None

    def process_cdata2(self, text):
        # very slow
        cdata_regexp = re.compile(r'<!\[CDATA\[?(.+?)\]\]>')
        while re.search(cdata_regexp, text) is not None:
            # print s
            found_cdata = re.search(cdata_regexp, text).group()
            name = re.search(cdata_regexp, text).group(1).strip()
            name_coded = base64.b64encode(name)
            text = text.replace(found_cdata, name_coded)
        return text

    def process_cdata(self, text):
        # hayaku !!!!!!
        CDATA_BEGIN = '<![CDATA['
        CDATA_END = ']]>'
        
        newdata = []
        
        for line in text.split(CDATA_BEGIN):
            items = line.split(CDATA_END)
            if len(items) > 1:
                items[0] = base64.b64encode(items[0].strip())
            for item in items:
                newdata.append(item)
        return ''.join(newdata)

    def __init__(self):
        self.is_animes = False
        self.is_ani = False
        self.is_titles = False
        self.is_title = False
        
        self.__animes = []
        self.ani = AniTitle()
        HTMLParser.HTMLParser.__init__(self)

    def feed(self, data):
        '''
        get the fuck out all cdata
        encode them by base64
        '''
#         data = data.replace('<![CDATA[', '"').replace(']]>', '"')
#         data = self.process_cdata(data)
        data = self.process_cdata(data)
        HTMLParser.HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        if tag == 'animes':
            self.is_animes = True
            
        if self.is_animes:
            attrs = Dict(attrs)
            if tag == 'anime':
                self.is_ani = True
                self.ani.ani_id = str(attrs['id'])
                self.ani.type = str(attrs['type'])
                pass_year(self.ani, str(attrs['year']))
            if tag == 'status':
                if str(attrs['watched']) == '1':
                    self.ani.completed = True
                else:
                    self.ani.completed = False
            if tag == 'neps':
                self.ani.eps = attrs['cnt']
            if tag == 'seps':
                self.ani.s_eps = attrs['cnt']
                
            if tag == 'titles':
                self.is_titles = True
            
            if self.is_titles:
                if tag == 'title':
                    if attrs['type'] == 'main':
                        # print 'is title starttag'
                        self.is_title = True
            if tag == 'dates':
                self.ani_date_start = attrs['start']
                self.ani.date_start = attrs['start']
                self.ani_date_finish = attrs['end']
                self.ani.date_end = attrs['end']
    
    def handle_endtag(self, tag):
        if tag == 'animes':
            self.is_animes = False
        
        if self.is_animes:
            if tag == 'anime':
                self.is_ani = False
            
            if tag == 'titles':
                self.is_titles = False
    
            if self.is_titles:
                if tag == 'title':
                    # print 'is title endtag'
                    self.is_title = False
    
    def handle_data(self, data):
        if self.is_animes:
            if self.is_ani:
                if self.is_titles:
                    # print 'is titles'
                    if self.is_title:
                        # self.ani_title = data
                        # print 'is title'
                        # print data
                        self.ani.ani_name = base64.b64decode(data)
                        pass
                    # self.ani[keys.ANI_NAME] = data
            else:
                if not self.ani.empty:
                    self.__animes.append(self.ani)
                    self.ani = AniTitle()
                # print self.ani_id, self.ani_type, self.ani_year
    
    @property
    def titles(self):
        return self.__animes

class TableParser(HTMLParser.HTMLParser):
    is_table = False
    is_row = False
    is_col = False

    rowdata = []
    tabledata = []

    def handle_starttag(self, tag, attrs):
        attrs = Dict(attrs)
        if tag == 'table': 
            if (attrs['id'] == 'stafflist' and
                attrs['class'] == 'stafflist'
                ):
                self.is_table = True

        if self.is_table:
            if tag == 'tr':
                self.is_row = True
                
        if self.is_row:
            if tag == 'td':
                self.is_col = True

    def handle_endtag(self, tag):
        if tag == 'table':
            self.is_table = False
            
        if self.is_table:
            if tag == 'tr':
                self.is_row = False
                
        if self.is_row:
            if tag == 'td':
                self.is_col = False
            
    def handle_data(self, data):
        if self.is_table:
            if self.is_row:
                if self.is_col:
                    self.rowdata.append(data)                    
            else:
                self.tabledata.append(self.rowdata)
                self.rowdata = []
                pass
                
    def get_titles(self):
        return self.tabledata

class AniDBMylistTypeParser(HTMLParser.HTMLParser):
    is_root = Bool()
    is_custom = Bool()
    is_userinfo = Bool()
    is_cats = Bool()
    is_animes = Bool()
    is_ani = Bool()
    is_status = Bool()
    is_neps = Bool()
    is_seps = Bool()
    is_titles = Bool()
    is_title = Bool()
    #
    is_tags = Bool()
    is_state = Bool()
    is_size = Bool()
    is_rating = Bool()
    is_reviews = Bool()
    #
    is_dates = Bool()
    #
    conditions = None
    
    def __init__(self):
        self.conditions = (
            self.is_root, self.is_custom, self.is_userinfo, self.is_cats,
            self.is_animes, self.is_ani, self.is_status, self.is_neps,
            self.is_seps, self.is_titles, self.is_title, self.is_tags,
            self.is_state, self.is_size, self.is_rating, self.is_reviews,
            self.is_dates)

        'memory effect'
        for item in self.conditions:
            item + False
        
        HTMLParser.HTMLParser.__init__(self)
    
    def feed(self, data):
        try:
            HTMLParser.HTMLParser.feed(self, data)
        except StopPleaseException:
            pass

    def handle_starttag(self, tag, attrs):
        attrs = Dict(attrs)
        if tag == 'root':
            self.is_root + True
#             print 'root'
        if self.is_root:
            if tag == 'custom':
                self.is_custom + True
#                 print 'custom'
            if self.is_custom:
                if tag == 'userinfo':
                    self.is_userinfo + True
#                     print 'userinfo'
            if tag == 'cats':
                self.is_cats + True
#                 print 'cats'
            if tag == 'animes':
                self.is_animes + True
#                 print 'animes'
            if self.is_animes:
                if tag == 'anime':
                    self.is_ani + True
#                     print 'anime'
                if self.is_ani:
                    if tag == 'status':
                        self.is_status + True
#                         print 'status'
                    if tag == 'neps':
                        self.is_neps + True
#                         print 'neps'
                    if tag == 'seps':
                        self.is_seps + True
#                         print 'seps'
                    if tag == 'titles':
                        self.is_titles + True
#                         print 'titles'
                    if self.is_titles:
                        if tag == 'title':
                            self.is_title + True
#                             print 'title'
                    if tag == 'tags':
                        self.is_tags + True
#                         print 'tags'
                    if tag == 'state':
                        self.is_state + True
#                         print 'state'
                    if tag == 'size':
                        self.is_size + True
#                         print 'size'
                    if tag == 'rating':
                        self.is_rating + True
#                         print 'rating'
                    if tag == 'reviews':
                        self.is_reviews + True
#                         print 'reviews'
                    if tag == 'dates':
                        self.is_dates + True
#                         print 'dates'
                        
        if reduce(lambda res, x : res and x, self.conditions, True):
            raise StopPleaseException()

    def handle_endtag(self, tag):
        pass
                    
    def handle_data(self, data):
        pass
    
    @property
    def type(self):
        lst = AniList()
        if reduce(lambda res, x : res and x, self.conditions, True):
            print 'MUYLIST PARSER LOL=====================>>'
            lst.type = listtype.MYLIST
            lst.name = 'mylist'
##            info = {}
##            info[keys.LIST_TYPE] = keys.FTYPE_MYLIST
##            info[keys.LIST_NAME] = 'mylist'
##            return info        
        else:
            #return None
            lst.type = listtype.UNKNOWN
        return lst

class AniDBTitleTypeParser(HTMLParser.HTMLParser):
    pass

class AniDBListTypeParser(HTMLParser.HTMLParser):
    is_header = False
    
    found = False
    is_person = False
    is_company = False
    namae = ''
    
    person_regexp = re.compile(r'Person:\s(.+)')
    company_regexp = re.compile(r'Company:\s(.+)')

    def handle_starttag(self, tag, attrs):
        
        if tag == 'table':
            attrs = Dict(attrs)
            if (attrs['id'] == 'stafflist' and
                attrs['class'] == 'stafflist' and
                not self.is_person                
                ):
                self.is_company = True
            elif (attrs['id'] == 'characterlist' and
                  attrs['class'] == 'characterlist' and
                  not self.is_company
                  ):
                self.is_person = True
            
        if tag == 'h1':
            self.is_header = True
        
    def handle_endtag(self, tag):
        if tag == 'h1':
            self.is_header = False
            
    def handle_data(self, data):
        if self.is_header:
            creator_str = data
            if re.search(self.person_regexp, creator_str) is not None:
                self.namae = re.search(self.person_regexp,
                                       creator_str).group(1).strip()
            if re.search(self.company_regexp, creator_str) is not None:
                self.namae = re.search(self.company_regexp,
                                       creator_str).group(1).strip()

    def get_type(self):
        lst = AniList()
        if self.is_person or self.is_company:
            lst.name = str(self.namae)
##            info = {keys.LIST_NAME : str(self.namae)}
            if self.is_person:
                lst.type = listtype.PERSON
##                info[keys.LIST_TYPE] = keys.FTYPE_PERSON
            if self.is_company:
                lst.type = listtype.COMPANY
##                info[keys.LIST_TYPE] = keys.FTYPE_COMPANY
#            return info
        else:
            lst.type = listtype.UNKNOWN
#            return None
        return lst
    
################################################################################
# PARSER TESTING
################################################################################

def test():
    import os
    curdir = os.path.abspath(os.path.curdir)
    file_ = '  AniDB.net   Person - Hanazawa Kana   .html'
    file_path = os.path.join(curdir, 'lists', file_)
    # file_path = '/home/alex/table3.html'
    with open(file_path) as f:
        html_text = ''.join(f.readlines())  # .replace('</tr><tr', '</tr> <tr')
        table_parser = PersonParser()
        table_parser.feed(html_text.decode('utf-8'))
        titles = table_parser.titles
    # print table_parser.get_tables()
    # print len(table_parser.get_tables())
        for t in titles:
            print t.ani_id, t.year, '\t' , t.ani_name
            
        print len(titles)
#     for t in titles:
#         print len(t), t
        
#     print 'row count:', table_parser.ROW_COUNT

def test1():
    import os
    import xml.etree.ElementTree as et
    from xml.etree.ElementTree import XMLParser as fuckyouall
    from xml.etree.ElementTree import ParseError as fuckit
    
    curdir = os.path.abspath(os.path.curdir)
    file_ = '  AniDB.net   Person - Hanazawa Kana   .html'
    file_path = os.path.join(curdir, 'lists', file_)
    with open(file_path) as f:
        tree = et.fromstringlist(f.readlines(), fuckyouall(html=True))
        root = tree.getroot()
        for table in root.findall('table'):
            print 'table'

def test3():
    import os
    curdir = os.path.abspath(os.path.curdir)
    file_ = 'mylist.xml'
    file_path = os.path.join(curdir, 'lists', file_)
    with open(file_path) as f:
        file_text = ''.join(f.readlines())
        parser = MylistParser()
        parser.feed(file_text)
        
        animes = parser.get_animes()
        
        for t in animes[0:50]:
            print t

def test4():
    text = 'spam spam spam <![CDATA[ Angel Beats! ]]> spam spam <![CDATA[ Another ]]> spam '
    mylistParser = MylistParser()
    print mylistParser.process_cdata2(text)
    
    print base64.b64decode(mylistParser.process_cdata2(text))
    
def test5():
    import os
#     file_ = '  AniDB.net   Person - Hanazawa Kana   .html'
    file_ = '  AniDB.net   Company - P.A. Works   .html'
    file_ = '  AniDB.net   Person - Maeda Jun   .html'
    file_ = 'mylist.xml'
    file_path = os.path.join(os.path.abspath(os.path.curdir), 'lists', file_)
    with open(file_path) as f:
        txt = ''.join(f.readlines())
        aniParser = AniDBListTypeParser()
        aniParser.feed(txt)
        print 'aniParser:', aniParser.get_type()
        if aniParser.get_type() == None:
            mylistTypeParser = MylistTypeParser()
            mylistTypeParser.feed(txt)
            print 'mylistTypeParser: ', mylistTypeParser.get_type()  

def test6():
    print 'lol'
    import os
#     file_ = '  AniDB.net   Person - Hanazawa Kana   .html'
    file_ = '  AniDB.net   Company - P.A. Works   .html'
#    file_ = '  AniDB.net   Person - Maeda Jun   .html'
#    file_ = 'mylist.xml'
    file_path = os.path.join(os.path.abspath(os.path.curdir), 'lists', file_)
    with open(file_path) as f:
        txt = ''.join(f.readlines())
        parser = CompanyParser()
        parser.feed(txt)
        animes = parser.animes
        
        for t in animes:
#             print t.year, t.ani_name
            print t.year, t.ani_name
    print listtype.PERSON
#     listtype.PERSON = 5
    print listtype.PERSON
    import collections
    Const = collections.namedtuple('Const', ['UNKNOWN', 'PERSON'])
    const = Const(0, 1)
    
#     print const.UNKNOWN
#     const.UNKNOWN = 5

def test7():
    import os
    curdir = os.path.abspath(os.path.curdir)
    file_ = '  AniDB.net   Company - Visual Art`s Key   .html'
    #file_ = '  AniDB.net   Company - Shaft   .html'
    file_path = os.path.join(curdir, 'lists', file_)
    with open(file_path) as f:
        file_text = ''.join(f.readlines())
        parser = CompanyParser()
        parser.feed(file_text)
        
        animes = parser.titles
        
        for t in animes[0:50]:
            print t.ani_id, t.ani_name

################################################################################
# LIST FUNCTIONS
################################################################################

def list_mylist(list_file, completed=False):
    with open(list_file) as f:
        fh = StringIO.StringIO()
        fh.write(f.read())
        titles = list_mylist4(fh, completed)
    return titles

def list_mylist4(xml_fh, completed=False):
    xml_text = xml_fh.getvalue()
    mylistParser = MylistParser()
    mylistParser.feed(xml_text)
    
    titles = mylistParser.titles
    return titles 

def list_company(list_file):
#     titles = None
    with open(list_file) as f:
        fh = StringIO.StringIO()
        fh.write(f.read())
        titles = list_company3(fh)
    return titles

def list_company4(html_fh):
    html_text = html_fh.getvalue()
    
    company_parser = CompanyParser()
    company_parser.feed(html_text.decode('utf-8'))
    titles = company_parser.titles
    print 'list_company', len(titles)
    
    return titles

def list_company3(html_fh):
    titles = list()
    title = AniTitle()
    
    html_text = html_fh.getvalue()
    soup = bs4.BeautifulSoup(html_text)
    
    table = soup.find('table', id='stafflist')
    rows = table.findAll('tr')
    for tr in rows:
        cols = tr.findAll('td')
        for td in cols:
            if td['class'] == ['name']:
                link = td.find('a')
                if (link):
                    ani_id_data = re.findall(r'show=anime&aid=(\d+)',
                                             link['href'])
                    if len(ani_id_data) == 1:
                        # print title
                        titles.append(title)
                        title = AniTitle()
                        title.ani_link = link['href']
                        title.ani_name = link.text
                        title.ani_id = ani_id_data[0]
            elif td['class'] == ['credit']:
                pass
#                 if not title.has_key('credit'):
#                     title['credit'] = list()
#                 title['credit'].append(td.text)
                # print td.text
            elif td['class'] == ['year']:
                # title['year'] = str(td.text)
                pass_year(title, str(td.text))
                # print 'year:', td.text
            elif td['class'] == ['type']:
                title.type = str(td.text)
                # print 'type:', td.text
            elif td['class'] == ['eps']:
                title.eps = str(td.text)
                # print 'eps:', td.text

        # print '####################################'
    titles.append(title)
    del titles[0]
    return titles

def list_person(list_file):
#     titles = None
    with open(list_file) as f:
        fh = StringIO.StringIO()
        fh.write(f.read())
        titles = list_person4(fh)
    return titles

def list_person4(html_fh):
    html_text = html_fh.getvalue()
    
    table_parser = PersonParser()
    table_parser.feed(html_text.decode('utf-8'))
    titles = table_parser.titles
    print 'list_person', len(titles)
    
    return titles

def list_check(list_file):
    with open(list_file) as f:
        fh = StringIO.StringIO()
        fh.write(f.read())
        info = list_check4(fh)
    return info

def list_check4(list_fh):
    file_text = list_fh.getvalue()
    aniParser = AniDBListTypeParser()
    aniParser.feed(file_text)
    lst = aniParser.get_type()
    if lst.type == listtype.UNKNOWN:
        lst = AniList()
        print 'MUYLIST LISTCHECK LOL=====================>>'
        mylistTypeParser = AniDBMylistTypeParser()
        mylistTypeParser.feed(file_text)
        lst = mylistTypeParser.type
    return lst

def list_check44(list_fh):
    file_text = list_fh.getvalue()
    aniParser = AniDBListTypeParser()
    aniParser.feed(file_text)
    info = aniParser.get_type()
    if info != None:
        return info
    else:
        mylistTypeParser = AniDBMylistTypeParser()
        mylistTypeParser.feed(file_text)
        info = mylistTypeParser.type
        if info != None:
            return info
    return None

def list_file3(file_path):
    with open(file_path) as f:
        fh = StringIO.StringIO()
        fh.write(f.read())
        file_status = list_check4(fh)
        if file_status['type'] == keys.FTYPE_COMPANY:
            lst = list_company3(fh)
            return lst
        elif file_status['type'] == keys.FTYPE_PERSON:
            lst = list_person4(fh)
            return lst
        elif file_status['type'] == keys.FTYPE_MYLIST:
            lst = list_mylist4(fh)
            return lst
        else:
            return None

################################################################################
# TESTING
################################################################################
        
def compare():
    main = os.path.join(os.curdir, 'lists')
    paths = {
        'jcs'   : os.path.join(main, '  AniDB.net   Company - J.C.Staff   .html'),
        'xbc'   : os.path.join(main, '  AniDB.net   Company - Xebec   .html'),
        'sht'   : os.path.join(main, '  AniDB.net   Company - Shaft   .html'),
        'mj'    : os.path.join(main, '  AniDB.net   Company - Xebec   .html'),
        'hk'    : os.path.join(main, '  AniDB.net   Person - Hanazawa Kana   .html'),
        'kh'    : os.path.join(main, '  AniDB.net   Person - Kamiya Hiroshi   .html'),
        'iu'    : os.path.join(main, '  AniDB.net   Person - Iguchi Yuka   .html'),
        'sh'    : os.path.join(main, '  AniDB.net   Person - Sakurai Harumi   .html'),
        'kr'    : os.path.join(main, '  AniDB.net   Person - Kugimiya Rie   .html'),
        'hs'    : os.path.join(main, '  AniDB.net   Person - Hino Satoshi   .html'),
        'on'    : os.path.join(main, '  AniDB.net   Person - Okamoto Nobuhiko   .html'),
        'mylist'    : os.path.join(main, 'mylist.xml')
        }
    print list_check('/home/alex/prog/lp2/lists/listcompare.pyc').type
#     hk = list_person(paths['hk'])
    #mylist = list_mylist(paths['mylist'])
    
#     print_list(hk[0:25])
    #print_list(mylist[0:25])
    
#    inter1 = list_inter([hk, mylist])
#    inter2 = list_inter([mylist, hk])
    
#    l1 = [{keys.ANI_ID : str(i)} for i in range(5)]
#    l2 = [{keys.ANI_ID : str(i)} for i in range(10)]
    
#    inter1 = list_inter([l1, l2])
#    inter2 = list_inter([l2, l1])
#    print inter1
#    print inter2
    
    # print len(hk)
    # print len(mylist)
    # print len(inter1)
    # print len(inter2)

#     hk2 = list_person44(paths['hk'])
#     print len(hk1), len(hk2)
#     print_list(hk1)
    
#     lst = hk1
#     for i in lst:
#         print i
#         print i[keys.YEAR], '%s' % (i[keys.ANI_NAME])
    
    # mylist = list_mylist(os.path.join(main, 'mylist.xml'), completed = False)
#     import timeit
#     times = 1
#     f1_t = timeit.Timer('func()', 'from __main__ import f1 as func').timeit(times)
#     f2_t = timeit.Timer('func()', 'from __main__ import f2 as func').timeit(times)
#     print 'f1 time: ', f1_t
#     print 'f2 time: ', f2_t  
    
# #    times = 5
# #    f1_t = Timer('func()', 'from __main__ import f1 as func').timeit(times)
# #    print 'f1:', f1_t
    
################################################################################
# COMPARE FUNCTIONS
################################################################################

def list_inter(lists):
    if len(lists) < 2:
        raise ValueError('must be >1 lists')
    
    lst = lists[0]
    store = dict(
                 (item.ani_id, item) for item in lst 
                 )
    inter = set([i.ani_id for i in lst])
    
    for lst in lists[1:]:
        inter = inter.intersection(set([item.ani_id for item in lst]))
        for item in lst:
            store[item.ani_id] = item
        
    output = []
    for item in inter:
        output.append(store[item])
    
    return output

def list_diff(lists):
    # titles are in first list, but not in second
    if len(lists) != 2:
        raise ValueError('must be 2 lists')

    lst1_set = set([item.ani_id for item in lists[0]])
    lst2_set = set([item.ani_id for item in lists[1]])
    differ = lst1_set.difference(lst2_set)
    
    output = []
    for item in lists[0]:
        if item.ani_id in differ:
            output.append(item)
            
    return output

def print_list(lst, uniq=True, field='year'):
    count = 0
    uniq_list = []
    
    for item in sorted(lst, key=lambda i : i.year):
        conditions = []
        data = (item.year, item.ani_name)
        if uniq:
            if data not in uniq_list:
                uniq_list.append(data)
                # conditions.append(1)
                conditions.append(True)
            else:
                # conditions.append(0)
                conditions.append(False)
        if not False in conditions:
        # if sum(conditions) == len(conditions):
        # if reduce(lambda res, x: res and x, conditions, True):
            print '%s %s' % (data[0], data[1])
            # print item
            # break
            count += 1
    print
    print 'count:', count

################################################################################
# LIST COMPARE PROGRAM
# A CERTAIN PROGRAM
################################################################################

class ListCompareView:
    # main window
    root = None
    
    frames = {}
    
    listboxes = {}
    buttons = {}
    radiobuttons = {}
    
    textlabels = {}
    modes = {}

    def close(self):
        self.root.destroy()
        self.root.quit()
    
    def __init__(self):
        self.createWidgets()
        
    def createWidgets(self):
        self.root = Tkinter.Tk()
        self.root.title('A Certain Title')
        w = 600
        h = 500
        self.root.geometry('%sx%s+0+0' % (w, h))

        self.modes['result_sort'] = Tkinter.StringVar()
        self.modes['result_sort'].set('year')
        
        self.modes['list_compare'] = Tkinter.StringVar()
        self.modes['list_compare'].set('intersect')
        
        self.textlabels['result_stat'] = Tkinter.StringVar()
        self.textlabels['result_stat'].set('count: 0')
        
        self.textlabels['awailable_stat'] = Tkinter.StringVar()
        self.textlabels['awailable_stat'].set('0 lists awailable')
        
        self.mk_main_frame()

    def mk_main_frame(self):
        self.frames['main'] = Tkinter.Frame(master=self.root, bg='black',bd=3)
        self.frames['main'].pack(fill='both', expand=True)
        self.mk_result_frame()
        self.mk_additional_frame()

    def mk_result_frame(self):
        main_frame = self.frames['main']

        self.frames['result'] = Tkinter.Frame(master=main_frame, bg='red',
                                            bd=3)
        self.frames['result'].pack(side='left', fill='both', expand=True)
        result_frame = self.frames['result']

        Tkinter.Label(result_frame, text='result list').pack(fill='both',
                                                            side='top')
        self.mk_statistic_frame()

        self.listboxes['result'] = Tkinter.Listbox(result_frame,
                                                selectmode=Tkinter.EXTENDED)
        result_listbox = self.listboxes['result']
        result_listbox.pack(side='left', fill='both', expand=True)
        
        res_scrollBar = Tkinter.Scrollbar(result_frame)
        res_scrollBar.pack(side='right', fill='y', expand=False)
        res_scrollBar['command'] = result_listbox.yview
        result_listbox['yscrollcommand'] = res_scrollBar.set

    def mk_statistic_frame(self):
        result_frame = self.frames['result']
        
        self.frames['statistic'] = Tkinter.Frame(result_frame, bg='blue', bd=3)
        self.frames['statistic'].pack(side='bottom', fill='both', expand=False)
        statistic_frame = self.frames['statistic']

        sort_label = Tkinter.Label(statistic_frame, text='sort:')
        sort_label.pack(side='left', fill='both')
        
        res_sort_mode = self.modes['result_sort']
        
        RADIO = (
            ('name', 'name'),
            ('year', 'year')
            )
        
        radio_opt = {'side' : 'left', 'fill' : 'none'}
        for title, value_ in RADIO:
            self.radiobuttons[title] = Tkinter.Radiobutton(statistic_frame,
                                text=title,
                                variable=res_sort_mode,
                                value=value_,
                                anchor='w')
            self.radiobuttons[title].pack(**radio_opt)

        exp_label = Tkinter.Label(statistic_frame, text='EXPAND')
        exp_label.pack(side='left', fill='both', expand=True)
        
        stat_label = Tkinter.Label(statistic_frame,
                      textvariable=self.textlabels['result_stat'])
        stat_label.pack(side='left', fill='both')

    def mk_additional_frame(self):
        main_frame = self.frames['main']
        self.frames['additional'] = Tkinter.Frame(master=main_frame,
                                                  bg='blue',
                                                  bd=3)
        self.frames['additional'].pack(side='right', fill='both', expand=False)
        
        self.mk_selected_frame()
        self.mk_awailable_frame()

    def mk_selected_frame(self):
        additinal_frame = self.frames['additional']
        
        self.frames['selected'] = Tkinter.Frame(additinal_frame, bg='green',
                                                bd=3)
        self.frames['selected'].pack(side='top', fill='both', expand=True)
        selected_frame = self.frames['selected']

        selectedLabel = Tkinter.Label(selected_frame, text='selected lists')
        selectedLabel.pack(fill='both')

        self.listboxes['selected'] = Tkinter.Listbox(selected_frame,
                                           selectmode=Tkinter.EXTENDED)
        sel_listbox = self.listboxes['selected']
        sel_listbox.pack(side='left', fill='both', expand=True)
        
        sel_scrollBar = Tkinter.Scrollbar(selected_frame)
        sel_scrollBar.pack(side='left', fill='y', expand=False)
        sel_scrollBar['command'] = sel_listbox.yview
        sel_listbox['yscrollcommand'] = sel_scrollBar.set

# #        style = ttk.Style()
# #        style.map('C.TButton',
# #                  foreground=[('pressed','red'),('active','blue')],
# #                  background=[('pressed','!disabled','black'),('active','white')]
# #            )
        BUTTONS = (
            ('UP', 'up'),
            ('DOWN', 'down'),
            ('LIST', 'list'),
            )
        
        # third button will be expand
        exp = 3
        for title, name in BUTTONS:
            exp -= 1
            self.buttons[name] = Tkinter.Button(selected_frame, text=title)
            self.buttons[name].pack(side='top', fill='both',
                                    expand=not bool(exp))
            
        mode_label = Tkinter.Label(selected_frame, text='mode:', anchor='n')
        mode_label.pack(side='top', fill='x')

        compare_mode = self.modes['list_compare']
                
        RADIO = (
            ('intersect', 'intersect'),
            ('differ',    'differ'),
            ('union',     'union')
            )

        radio_opt = {'side' : 'top', 'fill' : 'x'}
        for title, value_ in RADIO:
            Tkinter.Radiobutton(selected_frame, text=title,
                                variable=compare_mode, value=value_,
                                anchor='w').pack(**radio_opt)

    def mk_awailable_frame(self):
        additinal_frame = self.frames['additional']
        self.frames['awailable'] = Tkinter.Frame(additinal_frame, bg='red',
                                       bd=3)
        self.frames['awailable'].pack(side='top', fill='both', expand=True)
        awailable_frame = self.frames['awailable']

        self.mk_aw_buttons_frame()

        aw_label = Tkinter.Label(awailable_frame, text='awailable lists')
        aw_label.pack(side='top',fill='both')
        
        stat_label = Tkinter.Label(awailable_frame,
                            textvariable=self.textlabels['awailable_stat'])
        stat_label.pack(side='bottom', fill='both')

        self.listboxes['awailable'] = Tkinter.Listbox(awailable_frame,
                                                      selectmode=Tkinter.EXTENDED)
        
        aw_listbox = self.listboxes['awailable']
        aw_listbox.pack(side='left', fill='both', expand=True)
        aw_scrollBar = Tkinter.Scrollbar(awailable_frame)
        aw_scrollBar.pack(side='right', fill='y', expand=False)
        aw_scrollBar['command'] = aw_listbox.yview
        aw_listbox['yscrollcommand'] = aw_scrollBar.set

    def mk_aw_buttons_frame(self):
        awailable_frame = self.frames['awailable']
        self.frames['aw_buttons'] = Tkinter.Frame(awailable_frame,
                                        bg='yellow',
                                        bd=3)
        self.frames['aw_buttons'].pack(side='top', fill='x', expand=False)
        aw_buttons_frame = self.frames['aw_buttons']

        BUTTONS = (
            ('ADD',    'add'),
            ('DEL',    'del'),
            ('RELOAD', 'reload')
            )

        button_opt = {'side' : 'left', 'fill' : 'x', 'expand' : True}
        for title, name in BUTTONS:
            self.buttons[name] = Tkinter.Button(aw_buttons_frame, text=title)
            self.buttons[name].pack(**button_opt)

class ListCompareModel:
    view = None

    lists = {}

    def __init__(self, view_):
        self.view = view_
        
        self.lists['result'] = []
        self.lists['selected'] = []
        self.lists['awailable'] = []
        
    def upSelected(self):
        print 'UP'
        selected = self.lists['selected']
        listbox = self.view.listboxes['selected']
        
        indexes = map(int, listbox.curselection())
        print 'old', indexes
        new = [i for i in indexes]
        for i in indexes:
            if i != indexes.index(i):
                selected[i], selected[i-1] = selected[i-1], selected[i]
                new[indexes.index(i)] -= 1
        print 'new'
        self.displaySelected()

    def downSelected(self):
        print 'DOWN'
        selected = self.lists['selected']
        listbox = self.view.listboxes['selected']
        
        indexes = sorted(map(int, listbox.curselection()), reverse=True)
        print 'old', indexes
        new = [i for i in indexes]
        for i in indexes:
            if i != listbox.size() - indexes.index(i) - 1:
                selected[i], selected[i+1] = selected[i+1], selected[i]
                new[indexes.index(i)] += 1
        print 'new', new
        self.displaySelected()

    def listCompare(self):
        print 'LIST COMPARE'
        selected = self.lists['selected']
        result = self.lists['result']
        
        lists = []
        for item in selected:
            if item.type != listtype.UNKNOWN:
                if item.type == listtype.PERSON:
                    lst = list_person(item.path)
                elif item.type == listtype.COMPANY:
                    lst = list_company(item.path)
                elif item.type == listtype.MYLIST:
                    lst = list_mylist(item.path)
                lists.append(lst)
        res = []
        compareMode = self.view.modes['list_compare'].get()
        if compareMode == 'intersect':
            res = list_inter(lists)
        elif compareMode == 'differ':
            res = list_diff(lists[0:2])
        elif compareMode == 'union':
            for lst in lists:
                for item in lst:
                    res.append(item)
        print 'LENGTH', len(res)
        result[:] = res
        
        self.uniqResult()
        self.sortResult()
        self.displayResult()

    def addList(self):
        print 'ADD'
        listbox = self.view.listboxes['awailable']
        indexes = map(int, listbox.curselection())
        indexes.sort(reverse=True)
        awailable = self.lists['awailable']
        selected = self.lists['selected']
                      
        for i in indexes:
            selected.append(awailable.pop(i))

        self.sortAwailable()
        self.displayAwailable()
        self.displaySelected()

    def delList(self):
        print 'ADD'
        listbox = self.view.listboxes['selected']
        indexes = map(int, listbox.curselection())
        indexes.sort(reverse=True)
        awailable = self.lists['awailable']
        selected = self.lists['selected']
                      
        for i in indexes:
            awailable.append(selected.pop(i))

        self.sortAwailable()
        self.displayAwailable()
        self.displaySelected()

    def reloadLists(self):
        print 'RELOAD'        
        LISTS_DIR = 'lists'
        curdir = os.path.abspath(os.path.curdir)
        LISTS_PATH = os.path.normpath(os.path.join(curdir, LISTS_DIR))
        print LISTS_PATH
        awailable = self.lists['awailable']
        awailable[:] = []
        for list_file in os.listdir(LISTS_PATH):
            list_file_fullpath = os.path.join(LISTS_PATH, list_file)
            lst = list_check(list_file_fullpath)
            if lst.type != listtype.UNKNOWN:
                lst.path = list_file_fullpath
                print lst.type, lst.name
                awailable.append(lst)
                self.sortAwailable()
                self.displayAwailable()

    def sortAwailable(self):
        lst = self.lists['awailable']
        lst.sort(key=lambda item : (item.type, item.name))

    def displayAwailable(self):
        listbox = self.view.listboxes['awailable']
        textlabel = self.view.textlabels['awailable_stat']
        awailable = self.lists['awailable']
        
        listbox.delete(0, Tkinter.END)
        for item in awailable:
            listbox.insert(Tkinter.END, '%s' % (item.name))
        listbox.update()

        textlabel.set('%d lists awailable' % (len(awailable)))

    def displaySelected(self):
        listbox = self.view.listboxes['selected']
        selected = self.lists['selected']
        
        listbox.delete(0, Tkinter.END)
        for item in selected:
            listbox.insert(Tkinter.END, '%s' % (item.name))
        listbox.update()
        
        #self.sortResult()

    def sortResult(self):
        mode = self.view.modes['result_sort'].get()
        print mode
        if mode == 'year':
            function = lambda item : (item.year, item.ani_name)
        elif mode == 'name':
            function = lambda item : (item.ani_name, item.year)
        self.lists['result'].sort(key=function)

    def uniqResult(self):
        result = self.lists['result']
        uniq_dict = dict(
            (item.ani_id, item) for item in result
            )
        result[:] = uniq_dict.values()

    def displayResult(self):
        listbox = self.view.listboxes['result']
        result = self.lists['result']
        textlabel = self.view.textlabels['result_stat']
        
        listbox.delete(0, Tkinter.END)
        for item in result:
            listbox.insert(Tkinter.END, '%s %s' % (item.year, item.ani_name))
            
        textlabel.set('count: %i' % len(result))
        listbox.update()

    def resultSortChange(self, type_):
        self.view.modes['result_sort'].set(type_)
        self.sortResult()
        self.displayResult()

class ListCompareController:
    model = None
    view = None

    def __init__(self):
        self.view = ListCompareView()
        self.model = ListCompareModel(self.view)
        
        self.bind_handlers()
        
        self.view.root.protocol('WM_DELETE_WINDOW', self.close_handler)
        self.view.root.mainloop()

    def bind_handlers(self):
        up_button = self.view.buttons['up']
        up_button.bind("<Button-1>", self.up_handler)
        
        down_button = self.view.buttons['down']
        down_button.bind("<Button-1>", self.down_handler)

        list_button = self.view.buttons['list']
        list_button.bind("<Button-1>", self.list_handler)

        add_button = self.view.buttons['add']
        add_button.bind("<Button-1>", self.add_handler)

        del_button = self.view.buttons['del']
        del_button.bind("<Button-1>", self.del_handler)

        reload_button = self.view.buttons['reload']
        reload_button.bind("<Button-1>", self.reload_handler)

#        print self.view.radiobuttons
        sort_name_radiobutton = self.view.radiobuttons['name']
        sort_name_radiobutton.bind("<Button-1>", self.result_sort_handler_name)
        sort_year_radiobutton = self.view.radiobuttons['year']
        sort_year_radiobutton.bind("<Button-1>", self.result_sort_handler_year)

    def up_handler(self, event):
        print 'up handler'
        self.model.upSelected()

    def down_handler(self, event):
        print 'down handler'
        self.model.downSelected()

    def list_handler(self, event):
        print 'list handler'
        self.model.listCompare()

    def add_handler(self, event):
        print 'add handler'
        self.model.addList()

    def del_handler(self, event):
        print 'del handler'
        self.model.delList()

    def reload_handler(self, event):
        print 'reload handler'
        self.model.reloadLists()

    def result_sort_handler_name(self, event):
        print 'result sort handler name'
        self.model.resultSortChange('name')

    def result_sort_handler_year(self, event):
        print 'result sort handler year'
        self.model.resultSortChange('year')

    def close_handler(self):
        print 'close'
        self.view.close()

class ListCompareApp:
    controller = None

    def __init__(self):
        self.controller = ListCompareController()

################################################################################
# OTHER/OLD
################################################################################
    
def import_modules():
    modules_path = os.path.join(os.path.curdir, MODULES_DIR)
    if not (modules_path in sys.path):
        sys.path.append(modules_path)

def list_parse():
    try:
        from lxml import etree as etree
    except ImportError:
        import xml.etree.ElementTree as etree
    import gzip

    params = ['series_animedb_id', 'series_title', 'series_type', 'series_episodes',
     'my_id', 'my_watched_episodes', 'my_start_date', 'my_finish_date',
     'my_fansub_group', 'my_rated', 'my_score', 'my_dvd', 'my_storage',
     'my_status', 'my_comments', 'my_times_watched', 'my_rewatch_value',
     'my_downloaded_eps', 'my_tags', 'my_rewatching', 'my_rewatching_ep',
     'update_on_import']

    status = {'p' : 'Plan to Watch',
              'c' : 'Completed',
              'w' : 'Watching',
              'name' : 'my_status'
              }

    ALL = 1

    with gzip.open('zip/animelist_1391893533_-_3199957.xml.gz', 'r') as f:
        # tree = etree.parse(f)
        # root = tree.getroot()
        root = etree.fromstringlist(f)
        # print(len(titles))
        count = 0
        for title in root.findall('anime'):
            if (title.find(status['name']).text == status['c'] or ALL):
                name = title.find('series_title').text
                print(name)
                count += 1
        print()
        print('Count: ', count)    


def parse_info2222():
    try:
        # python2
        import urllib2
    except ImportError:
        # python3
        import urllib.request as urllib2
    import sys

    try:
        import mechanize
    except ImportError:
        modules_path = os.path.join(os.path.curdir, MODULES_DIR)
        if not (modules_path in sys.path):
            sys.path.append(modules_path)
            print(sys.path)
            try:
                import mechanize
            except ImportError:
                # lolwut?
                # modules dir corrupt?
                # restore from backup
                pass

    # #LOAD_DIR = ''
    
    anidb_link = 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid=6556'
    anidb_link = 'http://ru.wikipedia.org'
    br = mechanize.Browser()
    br.set_handle_robots(False)
    # headers = [('User-Agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:16.0) Gecko/20120815 Firefox/16.0')]
    # br.addheaders = headers
    page = br.open(anidb_link)
    request = br.request
    print request.header_items()
    print br.title()
    # print 'links count: ', len(br.links())
    # for link in br.links():
    #    print link.text
    
# #    page = urllib2.urlopen(anidb_link)
# #    page_content = page.read()
# #    print(page_content)
# #    
# #
# #    page_name = '1.html'
# #    save_path = os.path.join(LOAD_DIR, page_name)
# #    
# #    with open(save_path, 'w') as f:
# #        f.write(page_content)
# #    print('done')

################################################################################

if __name__ == '__main__':
    test7()
    #ListCompareApp()
#    import_modules()
    #compare()
#    prog = ListCompareApp()
    # path = '/media/Локальный диск/GAMES/unsortd/_r/'
 #   dir_ = 'Aura: Maryuuinkouga Saigo no Tatakai'
#    path = os.path.join(os.path.normpath(path), dir_)
    # make_dirs(path)
    pass
