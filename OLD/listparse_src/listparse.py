#!/usr/bin/env python2
##  PYTHON 2!!!!!!!!!!!!!!!!!!!

# -*- coding: utf-8 -*-

#==============================================================================#
# import abc
import os
import sys
#------------------------------------------------------------------------------#
import HTMLParser
#------------------------------------------------------------------------------#
import re
import StringIO
#------------------------------------------------------------------------------#
import shutil
#------------------------------------------------------------------------------#
import Tkinter
# import tkFileDialog
# import ttk

import parsers
from parsers import pass_year
import keys
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
            parser = InfoFileParser(fullpath)
            (title, year) = parser.parse()
            # (title, year) = parse_anidb_file(fullpath)
            titles.append((title, year))
    return titles

################################################################################
# PARSERS
################################################################################

class InfoFileParser:    
    def __init__(self, info_file_):
        self.info_file = info_file_
        print self.info_file
        
    def parse(self):
        filetype = 'anidb'
        if filetype == 'anidb':
            parser = self.AniDBparser
            
        return self.parse_file(self.info_file, parser)

    def parse_file(self, info_file, ParserClass):        
        with open(info_file) as html_file:
            html_text = ''.join(html_file.readlines())
            parser = ParserClass(html_text)
            (title, year) = (parser.title(), parser.year())
            print 'title:', title
            print 'year:', year
        return (title, year)
    
    class AniDBparser(HTMLParser.HTMLParser):
        def __init__(self, data):
            self.is_title = None
            self._title = None
            self.is_year = None
            self._year_data = list()
            
            HTMLParser.HTMLParser.__init__(self)
            data = data.decode('utf-8')
            self.feed(data)
            
        def handle_starttag(self, tag, attrs):
            if tag == 'h1':
                norm_attrs = map(str, unpack_list(attrs))
                title_attrs = ('class', 'anime')
                if set(norm_attrs).issuperset(title_attrs):
                    self.is_title = 1
            if tag == 'tr':
                # norm_attrs = map(str, unpack_list(attrs))
                norm_attrs = ''.join(map(str, unpack_list(attrs)))
                # year_attrs = ('class', 'g_odd year')
                # year_attrs = ('class', 'year')
                year_attrs = 'year'
                # if set(norm_attrs).issuperset(year_attrs):
                if year_attrs in norm_attrs:
                    self.is_year = 1
            
        def handle_endtag(self, tag):
            if tag == 'tr':
                self.is_year = 0
        
        def handle_data(self, data):
            if self.is_title:
                self._title = data
                self.is_title = 0
            if self.is_year:
                self._year_data.append(data)

        def title(self):
            title_ = re.findall(r'Anime:\s(.+)', self._title)
            if len(title_) > 0:
                return str(title_[0])
            else:
                return None

        def year(self):
            year_data = ''.join(self._year_data)
            year_ = re.findall(r'(\d{4})', year_data)
            if len(year_) > 0:
                return str(year_[0])
            else:
                return None
    
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
# LIST PARSERS
################################################################################
        
def list_mylist(list_file, completed=False):
#     titles = None
    with open(list_file) as f:
        fh = StringIO.StringIO()
        fh.write(f.read())
        titles = list_mylist3(fh, completed)
    return titles

def list_mylist44(list_file, completed=False):
#     titles = None
    with open(list_file) as f:
        fh = StringIO.StringIO()
        fh.write(f.read())
        titles = list_mylist4(fh, completed)
    return titles

def list_mylist3(xml_fh, completed=False):
    titles = []
    xml_text = xml_fh.getvalue()
    soup = bs4.BeautifulSoup(xml_text, features='xml')
    root = soup.find('root')
    lst = root.find('custom')

    while lst.nextSibling is not None:
        lst = lst.nextSibling
        if lst.name == 'animes':
            break

    for a_ in lst.findAll('anime'):
        title = {}
        
        pass_year(title, a_['year'])
        # print a_['year'],title
        title['type'] = a_['type']
        title[keys.ANI_ID] = a_['id']
        title[keys.EPS] = a_.find('neps')['cnt']

        if str(a_.find('status')['watched']) == '1':
            title[keys.COMPLETED] = True
        else:
            title[keys.COMPLETED] = False
        # print str(title_.find('status')['watched']), title['completed']
        for a_ in a_.find('titles').findAll('title'):
            if a_['type'] == 'main':
                title[keys.ANI_NAME] = a_.text
        if completed and title[keys.COMPLETED]:
            titles.append(title)
        if not completed:
            titles.append(title)
    return titles

def list_mylist4(xml_fh, completed=False):
    xml_text = xml_fh.getvalue()
    mylistParser = parsers.MylistParser()
    mylistParser.feed(xml_text)
    
    titles = mylistParser.get_animes()
    return titles 

def list_company(list_file):
#     titles = None
    with open(list_file) as f:
        fh = StringIO.StringIO()
        fh.write(f.read())
        titles = list_company3(fh)
    return titles

def list_company3(html_fh):
    titles = list()
    title = dict()
    
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
                        title = dict()
                        title['link'] = link['href']
                        title['name'] = link.text
                        title['anidb_id'] = ani_id_data[0]
            elif td['class'] == ['credit']:
                if not title.has_key('credit'):
                    title['credit'] = list()
                title['credit'].append(td.text)
                # print td.text
            elif td['class'] == ['year']:
                # title['year'] = str(td.text)
                pass_year(title, str(td.text))
                # print 'year:', td.text
            elif td['class'] == ['type']:
                title['type'] = str(td.text)
                # print 'type:', td.text
            elif td['class'] == ['eps']:
                title['episodes'] = str(td.text)
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
        titles = list_person3(fh)
    return titles

def list_person44(list_file):
#     titles = None
    with open(list_file) as f:
        fh = StringIO.StringIO()
        fh.write(f.read())
        titles = list_person4(fh)        
    return titles

def list_person4(html_fh):
    html_text = html_fh.getvalue()
    
    table_parser = parsers.PersonParser()
    table_parser.feed(html_text.decode('utf-8'))
    titles = table_parser.get_titles()
    
    return titles

def list_person3(html_fh):
    titles = list()
    html_text = html_fh.getvalue()
    
    soup = bs4.BeautifulSoup(html_text)
    table = soup.find('table', id='characterlist')
    rows = table.findAll('tr')
    for tr in rows:
        title = dict()
        cols = tr.findAll('td')
        for td in cols:
            if td['class'] == ['name']:
                link = td.find('a')
                if (link):
                    ani_id_regexp = re.compile(r'show=anime&aid=(\d+)')
                    ani_id_data = re.findall(ani_id_regexp,
                                             link['href'])
                    if len(ani_id_data) == 1:
                        title[keys.ANI_LINK] = link['href']
                        title[keys.ANI_NAME] = link.text
                        title[keys.ANI_ID] = ani_id_data[0]
                    char_id_regexp = re.compile(
                        r'show=character&charid=(\d+)')
                    char_id_data = re.findall(char_id_regexp,
                                              link['href'])
                    if len(char_id_data) == 1:
                        title[keys.CHAR_NAME] = link.text
                        title[keys.CHAR_LINK] = link['href']
                        title[keys.CHAR_ID] = char_id_data[0]
            elif td['class'] == ['year']:
                # title['year'] = str(td.text)
                pass_year(title, str(td.text))
            elif td['class'] == ['type']:
                title[keys.TYPE] = str(td.text)
            elif td['class'] == ['eps']:
                title[keys.EPS] = str(td.text)
        titles.append(title)
    del titles[0]
    return titles

FILE_TYPES = {
    'company' : 'company',
    'person'  : 'person',
    'mylist'  : 'mylist'
    }

def list_check(list_file):
#     info = None
    with open(list_file) as f:
        fh = StringIO.StringIO()
        fh.write(f.read())
        info = list_check3(fh)
    return info

def list_check3(list_fh):
#     info = {
#         'type' : None,
#         'name' : None
#         }
#     
    info = {}

    file_text = list_fh.getvalue()
    soup = bs4.BeautifulSoup(file_text)
    data = soup.find('h1', class_='creator')
    if data != None:
        # anidb
        person = re.findall(r'Person:\s(.+)', data.text)
        company = re.findall(r'Company:\s(.+)', data.text)
        if len(person) == 1:
            info[keys.LIST_NAME] = person[0]
        elif len(company) == 1:
            info[keys.LIST_NAME] = company[0]
        tables = soup.findAll('table')
        for table in tables:
            id_staff = table.has_attr('id')
            id_staff = id_staff and table.attrs['id'] == 'stafflist'
            class_staff = table.has_attr('class')
            class_staff = class_staff and 'stafflist' in table.attrs['class']
            if id_staff and class_staff:
                info[keys.LIST_TYPE] = 'company'
                return info
            id_char = table.has_attr('id')
            id_char = id_char and table.attrs['id'] == 'characterlist'
            class_char = table.has_attr('class')
            class_char = class_char and 'characterlist' in table.attrs['class']
            if id_char and class_char:
                info[keys.LIST_TYPE] = 'person'
                return info
        return None
    else:
        # mylist xml maybe?
        soup = bs4.BeautifulSoup(file_text, features='xml')
        root = soup.find('root')
        if root != None:
            names = ('custom', 'cats', 'animes')
            for name in names:
                item = root.find(name)
                if item == None:
                    return None
                info[keys.LIST_TYPE] = 'mylist'
                info[keys.LIST_NAME] = 'mylist'
            return info
    return None

def list_file3(file_path):
    with open(file_path) as f:
        fh = StringIO.StringIO()
        fh.write(f.read())
        file_status = list_check3(fh)
        if file_status['type'] == FILE_TYPES['company']:
            lst = list_company3(fh)
            return lst
        elif file_status['type'] == FILE_TYPES['person']:
            lst = list_person3(fh)
            return lst
        elif file_status['type'] == FILE_TYPES['mylist']:
            lst = list_mylist3(fh)
            return lst
        else:
            return None

################################################################################
# COMPARE FUNCTIONS
################################################################################

def compare():
    main = os.path.join(os.curdir, 'lists')
    paths = {
        'main'  : '/home/alex/programming/Python/listparse/lists',
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
    
    hk1 = list_mylist(paths['mylist'])  # list_person(paths['hk'])
    hk2 = list_mylist44(paths['mylist'])  # list_person44(paths['hk'])
    print len(hk1), len(hk2)
    
    lst = hk1
    for i in lst:
#         print i
        print i[keys.YEAR], '%s' % (i[keys.ANI_NAME])
    
    # mylist = list_mylist(os.path.join(main, 'mylist.xml'), completed = False)
    # print list_check(os.path.join(main, 'mylist.xml'))
    # print list_check(os.path.join(main, '  AniDB.net   Person - Hanazawa Kana   .html'))    
# #    jcs = list_studio(os.path.join(main, '  AniDB.net   Company - J.C.Staff   .html'))
# #    xbc = list_studio(os.path.join(main, '  AniDB.net   Company - Xebec   .html'))
    # sht = list_studio(os.path.join(main, '  AniDB.net   Company - Shaft   .html'))
    # print list_check(os.path.join(main, '  AniDB.net   Person - Hanazawa Kana   .html'))
        
    # print list_check(os.path.join(main, '  AniDB.net   Company - Shaft   .html'))
    
# #    times = 5
# #    f1_t = Timer('func()', 'from __main__ import f1 as func').timeit(times)
# #    print 'f1:', f1_t
    
    # mj = list_studio(os.path.join(main, '  AniDB.net   Person - Maeda Jun   .html'))
    # print list_check(os.path.join(main, '  AniDB.net   Person - Maeda Jun   .html'))
# #    kh = list_person(os.path.join(main, '  AniDB.net   Person - Kamiya Hiroshi   .html'))
# #    iu = list_person(os.path.join(main, '  AniDB.net   Person - Iguchi Yuka   .html'))
# #    sh = list_person(os.path.join(main, '  AniDB.net   Person - Sakurai Harumi   .html'))
# #    kr = list_person(os.path.join(main, '  AniDB.net   Person - Kugimiya Rie   .html'))
# #    hs = list_person(os.path.join(main, '  AniDB.net   Person - Hino Satoshi   .html'))
# #    on = list_person(os.path.join(main, '  AniDB.net   Person - Okamoto Nobuhiko   .html'))
    
    # hk_kh = list_inter([hk, kh])
    # kr_jcs = list_inter([kr, jcs])
    # print_list(hk_kh)
    # print_list(hk)
    # print_list(mj)
    # print_list(kr_jcs)
    # print_list(sh)
    # print_list(xbc)
    # print_list(list_inter([mylist, hk]))
    # print_list(list_diff([hk, mylist]))
    # print_list(mylist, field = 'year')

def list_inter(lists):
    if len(lists) < 2:
        raise ValueError('must be >1 lists')
    
    inter = set([item[keys.ANI_ID] for item in lists[0]])
    for lst in lists[1:]:
        lst_set = set([item[keys.ANI_ID] for item in lst])
        inter = inter.intersection(lst_set)
        
    output = []
    for item in lists[1]:
        if item[keys.ANI_ID] in inter:
            output.append(item)
    
    return output

def list_diff(lists):
    # titles are in first list, but not in second
    if len(lists) != 2:
        raise ValueError('must be 2 lists')

    lst1_set = set([item[keys.ANI_ID] for item in lists[0]])
    lst2_set = set([item[keys.ANI_ID] for item in lists[1]])
    differ = lst1_set.difference(lst2_set)
    
    output = []
    for item in lists[0]:
        if item['anidb_id'] in differ:
            output.append(item)
            
    return output

def print_list(lst, uniq=True, field='year'):
    count = 0
    uniq_list = []
    
    for item in sorted(lst, key=lambda i : i[field]):
        conditions = []
        data = (item[keys.YEAR], item[keys.ANI_NAME])
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

################################################################################
# LISTPARSE GUI
################################################################################

class ListCompare:
    # # THE BRAIN ##
    aw_lists = []
    sel_lists = []
    res_list = []
    
    def __init__(self):
        pass

class ListCompareGui:
    # main window
    root = None
    
    aw_listbox = None
    sel_listbox = None
    res_listbox = None
    
    aw_stat_text = None
    res_stat_text = None
    
    compareMode = None
    
    COMPARE_MODES = {
        'intersect' : '0',
        'differ'    : '1',
        'union'     : '2'
        }

    res_sortMode = None
    
    RES_SORT_MODES = {
        'name' : '0',
        'year' : '1'
        }
    
    def add_title_handler(self):
        pass
    
    def del_title_handler(self):
        pass
    
    def up_title_handler(self):
        pass
    
    def down_title_handler(self):
        pass
    
    def list_titles_handler(self):
        pass
    
    def reload_aw_handler(self):
        pass
    
    def __init__(self):
        self.createWidgets()
        
    def createWidgets(self):
        pass

# class ListCompareApp:
#     #listCompareGui
#     #listCompare
#     pass

class ListCompareApp:
    root = None

    aw_Listbox = None
    sel_Listbox = None
    res_Listbox = None

    aw_stat_Text = None
    res_list_Text = None
    #---------------
    compareMode = None
    res_sortMode = None
    
    settings = {}
    ###################
    aw_lists = []
    sel_lists = []
    res_list = []
    ###################

    COMPARE_MODES = {
        'intersect' : '0',
        'differ'    : '1',
        'union'     : '2'
        }
    
    RES_SORT_MODES = {
        'name' : '0',
        'year' : '1'
        }

    ################
    ### HANDLERS ###
    ################

    def add_t(self):
        items = sorted(map(int, self.aw_Listbox.curselection()), reverse=True)
        for i in items:
            self.sel_lists.append(self.aw_lists.pop(i))

        self.sort_aw()
        self.display_aw()
        self.display_sel()
        # self.display_lists()

    def del_t(self):
        items = sorted(map(int, self.sel_Listbox.curselection()),
                       reverse=True)
        for i in items:
            self.aw_lists.append(self.sel_lists.pop(i))
            
        self.sort_aw()
        self.display_aw()
        self.display_sel()
        # self.display_lists()
    
    def up_t(self):
        indexes = map(int, self.sel_Listbox.curselection())
        print 'old', indexes
        new = [i for i in indexes]
        for i in indexes:
            if i != indexes.index(i):
                (self.sel_lists[i],
                 self.sel_lists[i - 1]) = (self.sel_lists[i - 1],
                                           self.sel_lists[i])
                new[indexes.index(i)] -= 1
        print 'new', new
        # name = tkFileDialog.askopenfilename()
        self.display_sel()
        # self.display_lists()
        
        for i in new:
            self.sel_Listbox.selection_set(i, i)

    def down_t(self):
        indexes = sorted(map(int, self.sel_Listbox.curselection()),
                         reverse=True)
        print 'old', indexes
        new = [i for i in indexes]
        for i in indexes:
            if i != self.sel_Listbox.size() - indexes.index(i) - 1:
                (self.sel_lists[i],
                 self.sel_lists[i + 1]) = (self.sel_lists[i + 1],
                                         self.sel_lists[i])
                new[indexes.index(i)] += 1
        print 'new', new
        
        self.display_sel()
        # self.display_lists()
        for i in new:
            self.sel_Listbox.selection_set(i, i)

    def load_t(self):
        self.checkAwailableLists()
        self.display_lists()

    def list_t(self):
        lists = []
        for item in self.sel_lists:
            if item != None:
                if item[keys.LIST_TYPE] == 'person':
                    lst = list_person(item['file'])
                if item[keys.LIST_TYPE] == 'company':
                    lst = list_company(item['file'])
                if item[keys.LIST_TYPE] == 'mylist':
                    lst = list_mylist(item['file'])
                lists.append(lst)
        if (self.compareMode.get() == self.COMPARE_MODES['intersect']):
            res = list_inter(lists)
        elif (self.compareMode.get() == self.COMPARE_MODES['differ']):
            res = list_diff(lists[0:2])
        elif (self.compareMode.get() == self.COMPARE_MODES['union']):
            res = []
            for lst in lists:
                for item in lst:
                    res.append(item)
        self.res_list = res
        print_list(res)
        self.display_lists()
    
    def __init__(self):        
        self.root = Tkinter.Tk()
        self.root.title('A Certain Title')
        w = 600
        h = 500
        self.root.geometry('%sx%s+0+0' % (w, h))
        
        self.createWidgets()

        import_modules()
        self.reloadSettings()
        # self.checkAwailableLists()

        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.root.mainloop()

    def close(self):
        print 'close'
        self.root.destroy()
        self.root.quit()
        
    def reloadSettings(self):
        self.settings = {
            'LISTS_PATH' : 'lists'
            }
    
    def checkAwailableLists(self):
        lists_dir = self.settings['LISTS_PATH']
        lists_path = os.path.join(os.path.abspath(os.path.curdir), lists_dir)

        self.aw_lists = []
        self.sel_lists = []
        
        for item in os.listdir(lists_path):
            item_fullpath = os.path.join(lists_path, item)
            data = list_check(item_fullpath)
            if data != None:
                data['file'] = item_fullpath
                self.aw_lists.append(data)
                # print '',;
                # self.display_lists()
                self.sort_aw()
                self.display_aw()
                # self.root.update()
        self.sort_aw()
        self.display_aw()
        # self.display_lists()
        # print self.c

    ########################
    ### SORT AND DISPLAY ###
    ########################

    def sort_aw(self):
        # type, name
        # print self.aw_lists[0]
        self.aw_lists.sort(key=lambda item : (item[keys.LIST_TYPE], item[keys.LIST_NAME]))

    def sort_res(self):
        if self.res_sortMode.get() == self.RES_SORT_MODES['year']:
            self.res_list.sort(key=lambda item : item[keys.YEAR])
            print 'year'
        elif self.res_sortMode.get() == self.RES_SORT_MODES['name']:
            self.res_list.sort(key=lambda item : item[keys.ANI_NAME])
            print 'name'

    def sort_lists(self):
        self.sort_aw()
        self.sort_res()

    def display_aw(self):
        self.aw_Listbox.delete(0, Tkinter.END)
        for aw_list in self.aw_lists:
            self.aw_Listbox.insert(Tkinter.END, '%s' % (aw_list[keys.LIST_NAME]))
        self.aw_Listbox.update()
        self.aw_stat_Text.set('%d lists awailable' % (len(self.aw_lists)))

    def display_sel(self):
        self.sel_Listbox.delete(0, Tkinter.END)
        for sel_list in self.sel_lists:
            self.sel_Listbox.insert(Tkinter.END, '%s' % (sel_list[keys.LIST_NAME]))
        self.sel_Listbox.update()

    def display_res(self):
        self.res_Listbox.delete(0, Tkinter.END)
        uniq = []
        for item in self.res_list:
            if item[keys.ANI_NAME] not in uniq:
                uniq.append(item[keys.ANI_NAME])
                self.res_Listbox.insert(Tkinter.END, '%s %s' % (item[keys.YEAR], item[keys.ANI_NAME]))
                self.res_list_Text.set('count: %i' % len(self.res_list))
        self.res_list_Text.set('count: %i' % len(self.res_list))

    def display_lists(self):
        # print 'display'
        self.sort_lists()
        self.display_aw()
        self.display_sel()
        self.display_res()

    def backcall(self, event):
        print 'F pressed'

    ##################
    ### GUI CREATE ###
    ##################

    def createWidgets(self):
        # button_opt = {'side' : 'left', 'fill' : 'x', 'expand' : True}
        FRAME_BORDER = 3
        colors = {
            'main'       : 'black',
            'result'     : 'red',
            'st'         : 'blue',
            'add'        : 'blue',
            'sel'        : 'green',
            'aw'         : 'red',
            'aw_buttons' : 'yellow'
            }
        FRAMES = {
            'main' : {
                'opt'  : {
                    'bg' : colors['main'],
                    'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'fill'   : 'both',
                    'expand' : True
                    }
                },
            'res' : {
                'opt' : {
                    'bg' : colors['result'],
                    'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'side'   : 'left',
                    'fill'   : 'both',
                    'expand' : True
                    }
                },
            'add' : {
                'opt' : {
                    'bg' : colors['add'],
                    'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'side'   : 'right',
                    'fill'   : 'both',
                    'expand' : False
                    }
                },
            'sel' : {
                'opt' : {
                    'bg' : colors['sel'],
                    'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'side'   : 'top',
                    'fill'   : 'both',
                    'expand' : True
                    }
                },
            'aw' : {
                'opt' : {
                    'bg' : colors['aw'],
                    'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'side'   : 'right',
                    'fill'   : 'both',
                    'expand' : False
                    }
                },
            'st' : {
                'opt' : {
                    'bg' : colors['st'],
                    'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'side'   : 'bottom',
                    'fill'   : 'both',
                    'expand' : False
                    }
                }
            }
        
        main_Frame = Tkinter.Frame(master=self.root, **FRAMES['main']['opt'])
        main_Frame.pack(**FRAMES['main']['pack'])
        ##############################################################
        res_Frame = Tkinter.Frame(master=main_Frame, **FRAMES['res']['opt'])
        res_Frame.pack(**FRAMES['res']['pack'])
        
        Tkinter.Label(res_Frame, text='result list').pack(fill='both',
                                                            side='top')

        self.res_list_Text = Tkinter.StringVar()
        self.res_list_Text.set('count: 0')

        st_Frame = Tkinter.Frame(res_Frame, **FRAMES['st']['opt'])
        st_Frame.pack(**FRAMES['st']['pack'])

        Tkinter.Label(st_Frame, text='sort:').pack(side='left', fill='both')
        self.res_sortMode = Tkinter.StringVar()
        self.res_sortMode.set(self.RES_SORT_MODES['year'])
        
        RADIO = (
            ('name', self.RES_SORT_MODES['name']),
            ('year', self.RES_SORT_MODES['year'])
            )
        
        radio_opt = {'side' : 'left', 'fill' : 'none'}
        for title, value_ in RADIO:
            Tkinter.Radiobutton(st_Frame, text=title,
                                variable=self.res_sortMode, value=value_,
                                anchor='w').pack(**radio_opt)

        Tkinter.Label(st_Frame, text='').pack(side='left',
                                                    fill='both',
                                                    expand=True)
        Tkinter.Label(st_Frame,
                      textvariable=self.res_list_Text).pack(side='left',
                                                              fill='both')
        
        self.res_Listbox = Tkinter.Listbox(res_Frame,
                                                selectmode=Tkinter.EXTENDED)
        self.res_Listbox.pack(side='left', fill='both', expand=True)
        
        res_scrollBar = Tkinter.Scrollbar(res_Frame)
        res_scrollBar.pack(side='right', fill='y', expand=False)
        res_scrollBar['command'] = self.res_Listbox.yview
        self.res_Listbox['yscrollcommand'] = res_scrollBar.set
        ##############################################################
        add_Frame = Tkinter.Frame(master=main_Frame, **FRAMES['add']['opt'])
        add_Frame.pack(**FRAMES['add']['pack'])
        ##############################################################
        sel_Frame = Tkinter.Frame(add_Frame, **FRAMES['sel']['opt'])
        sel_Frame.pack(**FRAMES['sel']['pack'])

        selectedLabel = Tkinter.Label(sel_Frame, text='selected lists')
        selectedLabel.pack(fill='both')

        self.sel_Listbox = Tkinter.Listbox(sel_Frame,
                                           selectmode=Tkinter.EXTENDED)
        self.sel_Listbox.pack(side='left', fill='both', expand=True)
        
        sel_scrollBar = Tkinter.Scrollbar(sel_Frame)
        sel_scrollBar.pack(side='left', fill='y', expand=False)
        sel_scrollBar['command'] = self.sel_Listbox.yview
        self.sel_Listbox['yscrollcommand'] = sel_scrollBar.set

# #        style = ttk.Style()
# #        style.map('C.TButton',
# #                  foreground=[('pressed','red'),('active','blue')],
# #                  background=[('pressed','!disabled','black'),('active','white')]
# #            )
        BUTTONS = (
            ('UP', self.up_t),
            ('DOWN', self.down_t),
            ('LIST', self.list_t),
            )
        
        # third button will be expand
        exp = 3
        for title, command_ in BUTTONS:
            exp -= 1
            Tkinter.Button(sel_Frame, text=title,  # #style = 'C.TButton',
                           command=command_).pack(side='top',
                                                    fill='both',
                                                    expand=not bool(exp))
            
        Tkinter.Label(sel_Frame, text='mode:',
                      anchor='n').pack(side='top', fill='x')

        self.compareMode = Tkinter.StringVar()
        self.compareMode.set(self.COMPARE_MODES['intersect'])
        
        RADIO = (
            ('intersect', self.COMPARE_MODES['intersect']),
            ('differ', self.COMPARE_MODES['differ']),
            ('union', self.COMPARE_MODES['union'])
            )

        radio_opt = {'side' : 'top', 'fill' : 'x'}
        for title, value_ in RADIO:
            Tkinter.Radiobutton(sel_Frame, text=title,
                                variable=self.compareMode, value=value_,
                                anchor='w').pack(**radio_opt)
        ##############################################################
        aw_Frame = Tkinter.Frame(add_Frame, bg=colors['aw'],
                                       bd=FRAME_BORDER)
        aw_Frame.pack(side='top', fill='both', expand=True)
        ##############################################################
        aw_buttonsFrame = Tkinter.Frame(aw_Frame,
                                        bg=colors['aw_buttons'],
                                        bd=FRAME_BORDER)
        aw_buttonsFrame.pack(side='top', fill='x', expand=False)

        BUTTONS = (
            ('ADD', self.add_t),
            ('DEL', self.del_t),
            ('RELOAD', self.load_t)
            )

        button_opt = {'side' : 'left', 'fill' : 'x', 'expand' : True}
        for title, command_ in BUTTONS:
            Tkinter.Button(aw_buttonsFrame, text=title,
                           command=command_).pack(**button_opt)
        
        Tkinter.Label(aw_Frame, text='awailable lists').pack(side='top',
                                                               fill='both')

        self.aw_stat_Text = Tkinter.StringVar()
        self.aw_stat_Text.set('0 lists awailable')

        Tkinter.Label(aw_Frame,
                      textvariable=self.aw_stat_Text).pack(side='bottom',
                                                             fill='both')

        self.aw_Listbox = Tkinter.Listbox(aw_Frame,
                                          selectmode=Tkinter.EXTENDED)
        self.aw_Listbox.pack(side='left', fill='both', expand=True)
        aw_scrollBar = Tkinter.Scrollbar(aw_Frame)
        aw_scrollBar.pack(side='right', fill='y', expand=False)
        aw_scrollBar['command'] = self.aw_Listbox.yview
        self.aw_Listbox['yscrollcommand'] = aw_scrollBar.set

#        self.root.bind('f', self.backcall)

################################################################################

################################################################################
# OTHER
################################################################################
    
def import_modules():
    modules_path = os.path.join(os.path.curdir, MODULES_DIR)
    if not (modules_path in sys.path):
        sys.path.append(modules_path)

################################################################################

if __name__ == '__main__':
#    import_modules()
    compare()
#    prog = ListCompareApp()
    # path = '/media/Локальный диск/GAMES/unsortd/_r/'
 #   dir_ = 'Aura: Maryuuinkouga Saigo no Tatakai'
#    path = os.path.join(os.path.normpath(path), dir_)
    # make_dirs(path)
    pass
