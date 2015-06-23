#!/usr/bin/env python2
##  PYTHON 2!!!!!!!!!!!!!!!!!!!

# -*- coding: utf-8 -*-

#==============================================================================#
import os
import sys
import re
import StringIO
# import tkFileDialog
# import ttk

#import parsers
from parsers import *
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
    
################################################################################
# LIST PARSERS
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
# COMPARE FUNCTIONS
################################################################################

main = os.path.join(os.curdir, 'lists')
paths = {
        'jcs'   : os.path.join(main, '  AniDB.net   Company - J.C.Staff   .html'),
        'xbc'   : os.path.join(main, '  AniDB.net   Company - Xebec   .html'),
        'sht'   : os.path.join(main, '  AniDB.net   Company - Shaft   .html'),
        'mj'    : os.path.join(main, '  AniDB.net   Person - Maeda Jun   .html'),
        'hk'    : os.path.join(main, '  AniDB.net   Person - Hanazawa Kana   .html'),
        'kh'    : os.path.join(main, '  AniDB.net   Person - Kamiya Hiroshi   .html'),
        'iu'    : os.path.join(main, '  AniDB.net   Person - Iguchi Yuka   .html'),
        'sh'    : os.path.join(main, '  AniDB.net   Person - Sakurai Harumi   .html'),
        'kr'    : os.path.join(main, '  AniDB.net   Person - Kugimiya Rie   .html'),
        'hs'    : os.path.join(main, '  AniDB.net   Person - Hino Satoshi   .html'),
        'on'    : os.path.join(main, '  AniDB.net   Person - Okamoto Nobuhiko   .html'),
        'mylist'    : os.path.join(main, 'mylist.xml')
        }
        
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
#    import_modules()
    compare()
#    prog = ListCompareApp()
    # path = '/media/Локальный диск/GAMES/unsortd/_r/'
 #   dir_ = 'Aura: Maryuuinkouga Saigo no Tatakai'
#    path = os.path.join(os.path.normpath(path), dir_)
    # make_dirs(path)
    pass
