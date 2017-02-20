#!/usr/bin/env python2
##  PYTHON 2!!!!!!!!!!!!!!!!!!!

# -*- coding: utf-8 -*-

import listparse

######################################################################
# OTHER/OLD
######################################################################

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

    ##LOAD_DIR = ''
    
    anidb_link = 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid=6556'
    anidb_link = 'http://ru.wikipedia.org'
    br = mechanize.Browser()
    br.set_handle_robots(False)
    #headers = [('User-Agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:16.0) Gecko/20120815 Firefox/16.0')]
    #br.addheaders = headers
    page = br.open(anidb_link)
    request = br.request
    print request.header_items()
    print br.title()
    #print 'links count: ', len(br.links())
    #for link in br.links():
    #    print link.text
    
##    page = urllib2.urlopen(anidb_link)
##    page_content = page.read()
##    print(page_content)
##    
##
##    page_name = '1.html'
##    save_path = os.path.join(LOAD_DIR, page_name)
##    
##    with open(save_path, 'w') as f:
##        f.write(page_content)
##    print('done')

######################################################################
######################################################################

def res_copy_script():
    main_save = '/media/Локальный диск/GAMES/wh/wh_ehd7_f/'
    titles = os.path.join(main_save, 'titles')

    def a():
        save = os.path.join(main_save, 'a')
        res = ResCopy()
        res.set_dirs(save, titles)
        res.add('/media/Локальный диск/GAMES/unsortd/_/')
        #res.add('/media/Index/a')
        #res.add('/media/Reserve/a')
        #res.add('/media/temp')
        #res.add('/media/Index1/a')
        #res.add('/media/temp1')
        #res.add('/media/temp2')
        res.start()

    def m():
        save = os.path.join(main_save, 'm')
        #res = ResCopy()
        #res.set_dirs(save, titles)
        #res.add('/media/Index/m')
        #res.start()

    a()
    m()

######################################################################
# LIST PARSERS
######################################################################

def compare():
    main = '/home/alex/programming/Python/listparse/lists'
    mylist = list_mylist(os.path.join(main, 'mylist.xml'), completed = False)
    
##    jcs = list_studio(os.path.join(main, '  AniDB.net   Company - J.C.Staff   .html'))
##    xbc = list_studio(os.path.join(main, '  AniDB.net   Company - Xebec   .html'))
    #sht = list_studio(os.path.join(main, '  AniDB.net   Company - Shaft   .html'))
    hk = list_person(os.path.join(main, '  AniDB.net   Person - Hanazawa Kana   .html'))
##    kh = list_person(os.path.join(main, '  AniDB.net   Person - Kamiya Hiroshi   .html'))
##    iu = list_person(os.path.join(main, '  AniDB.net   Person - Iguchi Yuka   .html'))
##    sh = list_person(os.path.join(main, '  AniDB.net   Person - Sakurai Harumi   .html'))
##    kr = list_person(os.path.join(main, '  AniDB.net   Person - Kugimiya Rie   .html'))
##    hs = list_person(os.path.join(main, '  AniDB.net   Person - Hino Satoshi   .html'))
##    on = list_person(os.path.join(main, '  AniDB.net   Person - Okamoto Nobuhiko   .html'))
    
    #hk_kh = list_inter([hk, kh])
    #kr_jcs = list_inter([kr, jcs])
    #print_list(hk_kh)
    print_list(hk)
    #print_list(kr_jcs)
    #print_list(sh)
    #print_list(xbc)
    #print_list(list_inter([mylist, hk]))
    #print_list(list_diff([hk, mylist]))
    #print_list(mylist, field = 'year')

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
        #tree = etree.parse(f)
        #root = tree.getroot()
        root = etree.fromstringlist(f)
        #print(len(titles))
        count = 0
        for title in root.findall('anime'):
            if (title.find(status['name']).text == status['c'] or ALL):
                name = title.find('series_title').text
                print(name)
                count += 1
        print()
        print('Count: ', count)
    
if __name__ == '__main__':
    import_modules()
    #list_file = '/home/alex/programming/Python/listparse/zip/  AniDB.net   Person - Hanazawa Kana   .html'
    #list_person(list_file)
    #list_file = '/home/alex/programming/Python/listparse/zip/  AniDB.net   Company - J.C.Staff   .html'
    #res_copy(0,0)
    #res_copy_script()
#    list_studio(list_file)

    compare()
    
    #list_parse()
    #dir_ = 'Stella Jogakuin Koutouka C3-bu'
    #main_dir = os.path.join('/media/Локальный диск/GAMES/unsortd/_/',dir_)
    #make_dirs(main_dir)
    

####>>> lst = [[1,2,3],[3,4,5]]
####>>> lst
####[[1, 2, 3], [3, 4, 5]]
####>>> map(str,lst)
####['[1, 2, 3]', '[3, 4, 5]']
####>>> map(str,map(str,lst))
####['[1, 2, 3]', '[3, 4, 5]']
####>>> map(lambda l:map(str,l),lst)
####[['1', '2', '3'], ['3', '4', '5']]
####
####
####>>> lst2 = [[[1,2,3],[4,5,6]],[[1,2,3],[4,5,6]]]
####>>> str(lst2)
####'[[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]]'
####>>> map(str, lst2)
####['[[1, 2, 3], [4, 5, 6]]', '[[1, 2, 3], [4, 5, 6]]']
####>>> map(lambda ll:str(ll), lst2)
####['[[1, 2, 3], [4, 5, 6]]', '[[1, 2, 3], [4, 5, 6]]']
####>>> map(lambda ll:map(str,ll), lst2)
####[['[1, 2, 3]', '[4, 5, 6]'], ['[1, 2, 3]', '[4, 5, 6]']]
####>>> map(lambda ll:map(lambda lll: map(str, lll),ll), lst2)
####[[['1', '2', '3'], ['4', '5', '6']], [['1', '2', '3'], ['4', '5', '6']]]
