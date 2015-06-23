'''
Created on 15.03.2014

@author: alex
'''

import HTMLParser
import re
import base64

import os

import keys

def _pass_year(title, date):
    DATE_SEPARATOR = '-'
    date_lst = date.replace(' ', '').split(DATE_SEPARATOR)
    
    if len(date_lst) == 1:
        title['year'] = date_lst[0]
        title['year_start'] = date_lst[0]
        title['year_finish'] = date_lst[0]
    if len(date_lst) == 2:
        title['year'] = date_lst[0]
        title['year_start'] = date_lst[0]
        title['year_finish'] = date_lst[1]

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
    
    title[keys.YEAR] = year
    title[keys.YEAR_START] = start
    title[keys.YEAR_FINISH] = finish
    
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

class Dict():
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

class PersonParser(HTMLParser.HTMLParser):
    is_table = False
    is_row = False
    is_col = False

    rowdata = []
    tabledata = []

    CHAR_LINK = 'http://anidb.net/perl-bin/animedb.pl\?show=character&charid='
    CHAR_LINK_PATTERN = re.compile(CHAR_LINK + '(\d+)')
    ANI_LINK = 'http://anidb.net/perl-bin/animedb.pl\?show=anime&aid='
    ANI_LINK_PATTERN = re.compile(ANI_LINK + '(\d+)')

    title = {}
    titles = []

    charid_zero = False

    is_char = False
    is_char_link = False
    char_link = ''
    char_id = ''
    is_ani = False
    is_ani_link = False
    ani_link = ''
    ani_id = ''
    
    char_name = ''
    
    is_type = False
    is_eps = False
    is_year = False
        
    def feed(self, data):
        data = data.replace('</tr><tr', '</tr> <tr')
        HTMLParser.HTMLParser.feed(self, data)
    
    def handle_starttag(self, tag, attrs):
        attrs = Dict(attrs)
        
        if tag == 'table':
            if attrs['id'] == 'characterlist':
                self.is_table = True
                
        if self.is_table:
            if tag == 'tr':
                self.is_row = True
                if attrs['id'] == 'charid_0':
                    self.charid_zero = True
                    
        if self.is_row:
            if tag == 'td':
                self.is_col = True
        
#         if self.is_row:
#             if tag == 'td' and attrs['class'] == 'comment':
#                 self.is_row = False
        
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
                    self.char_id = self.CHAR_LINK_PATTERN.findall(link)[0]
                    self.char_link = link
                    self.is_char_link = True

        if self.is_ani:
            if tag == 'a':
                link = attrs['href']
                if self.ANI_LINK_PATTERN.match(link):
                    self.ani_id = self.ANI_LINK_PATTERN.findall(link)[0]
                    self.ani_link = link
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
                self.ani_id = ''
                self.is_ani_link = False
            
    def handle_data(self, data):
        if self.is_table:
            if self.is_row:
                if self.is_col:
                    if self.is_char:
                        if self.charid_zero:
                            self.char_name = data.lstrip().rstrip()
                            self.charid_zero = False
                            self.is_char = False
                        if self.is_char_link:
                            self.char_name = data
                            self.is_char = False
                    if self.is_ani:
                        if self.is_ani_link:
#                             print 'char id:', self.char_id
                            self.title[keys.CHAR_ID] = str(self.char_id)
#                             print 'char link:', self.char_link
                            self.title[keys.CHAR_LINK] = str(self.char_link)
#                             print 'char namae2:', self.char_name
                            self.title[keys.CHAR_NAME] = self.char_name
#                             print 'ani id:', self.ani_id
                            self.title[keys.ANI_ID] = str(self.ani_id)
#                             print 'ani link:', self.ani_link
                            self.title[keys.ANI_LINK] = str(self.ani_link)
#                             print 'ani namae:', data
                            self.title[keys.ANI_NAME] = data
                            
                            self.is_ani = False
                    if self.is_type:
                        self.title[keys.TYPE] = str(data)
#                         print 'type:', data
                        self.is_type = False
                    if self.is_eps:
                        self.title[keys.EPS] = str(data)
#                         print 'eps:', data
                        self.is_eps = False
                    if self.is_year:
                        year = str(data)
                        pass_year(self.title, year)
#                         self.title[keys.YEAR] = str(data)
#                         print 'year:', data
                        self.is_year = False
#                         print '##########################################'
#                    self.rowdata.append(data)
            else: 
                # self.tabledata.append(self.rowdata)
                # self.rowdata = []
                if len(self.title) != 0:
                    self.titles.append(self.title)
                    self.title = {}

    def get_titles(self):
        # return self.tabledata
        return self.titles
        # return self.tables
        # return self.rowdata

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
    
    ani_id = ''
    ani_type = ''
    ani_year = ''
    ani_title = ''
    ani_date_start = ''
    ani_date_finish = ''
    
    eps = ''
    s_eps = ''
    
    comleted = False    
    
    animes = []
    ani = {}

    def process_cdata(self, text):
        cdata_regexp = re.compile(r'<!\[CDATA\[?(.+?)\]\]>')
        s = text
        while re.search(cdata_regexp, s) is not None:
            # print s
            found_cdata = re.search(cdata_regexp, s).group()
            name = re.search(cdata_regexp, s).group(1).strip()
            name_coded = base64.b64encode(name)
            s = s.replace(found_cdata, name_coded)
        return s

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        # print HTMLParser.HTMLParser

    def feed(self, data):
        # get the fuck out all cdata
        # data = data.replace('<![CDATA[', '"').replace(']]>', '"')
        data = self.process_cdata(data)
        HTMLParser.HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        if tag == 'animes':
            self.is_animes = True
            
        if self.is_animes:
            attrs = Dict(attrs)
            if tag == 'anime':
                self.is_ani = True
                
                self.ani_id = attrs['id']
                self.ani[keys.ANI_ID] = str(attrs['id'])
                 
                self.ani_type = attrs['type']
                self.ani[keys.TYPE] = str(attrs['type'])
                
                self.ani_year = attrs['year']
                pass_year(self.ani, str(attrs['year']))
            if tag == 'status':
                if str(attrs['watched']) == '1':
                    self.comleted = True
                else:
                    self.comleted = False
                self.ani[keys.COMPLETED] = self.comleted 
            if tag == 'neps':
                self.eps = attrs['cnt']
                self.ani[keys.EPS] = self.eps 
            if tag == 'seps':
                self.s_eps = attrs['cnt']
                self.ani[keys.S_EPS] = self.s_eps
                
            if tag == 'titles':
                self.is_titles = True
            
            if self.is_titles:
                if tag == 'title':
                    if attrs['type'] == 'main':
                        # print 'is title starttag'
                        self.is_title = True
            if tag == 'dates':
                self.ani_date_start = attrs['start']
                self.ani[keys.DATE_START] = attrs['start']
                self.ani_date_finish = attrs['end']
                self.ani[keys.DATE_FINISH] = attrs['end']
    
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
                        self.ani[keys.ANI_NAME] = base64.b64decode(data)
                        pass
                    # self.ani[keys.ANI_NAME] = data
            else:
                if len(self.ani) != 0:
                    self.animes.append(self.ani)
                    self.ani = {}
                # print self.ani_id, self.ani_type, self.ani_year
    
    def get_animes(self):
        return self.animes

class PersonParser1(HTMLParser.HTMLParser):
    is_table = False
    is_row = False
    is_col = False

    rowdata = []
    tabledata = []

    def handle_starttag(self, tag, attrs):
        attrs = Dict(attrs)
        if tag == 'table': 
            table = attrs['id'] == 'characterlist' 
            table = table and attrs['class'] == 'characterlist'
            if table:
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

def test():
    curdir = os.path.abspath(os.path.curdir)
    file_ = '  AniDB.net   Person - Hanazawa Kana   .html'
    file_path = os.path.join(curdir, 'lists', file_)
    # file_path = '/home/alex/table3.html'
    with open(file_path) as f:
        html_text = ''.join(f.readlines())  # .replace('</tr><tr', '</tr> <tr')
        table_parser = PersonParser()
        table_parser.feed(html_text.decode('utf-8'))
        titles = table_parser.get_titles()
    # print table_parser.get_tables()
    # print len(table_parser.get_tables())
        for t in titles[0:]:
            print len(t), t[keys.YEAR], t[keys.CHAR_NAME], '\t' , t[keys.ANI_NAME]
            
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
    import base64
    import re
    text = 'spam spam spam <![CDATA[ Angel Beats! ]]> spam spam <![CDATA[ Another ]]> spam '
    
    def lol(ss):
        cdata_regexp = re.compile(r'<!\[CDATA\[?(.+?)\]\]>')
        s = ss
        while re.search(cdata_regexp, s) is not None:
        # while re.search(cdata_regexp, s) is not None:
            print s
            print re.search(cdata_regexp, s)
            found_cdata = re.search(cdata_regexp, s).group()
            print found_cdata 
            name = re.search(cdata_regexp, text).group(1).strip()
            print name
            name_coded = base64.b64encode(name)
            s = s.replace(found_cdata, name_coded)
        return s
    
    print lol(text)
    
    print base64.b64decode(lol(text))

if __name__ == '__main__':
    pass
    # test3()
    # test1()
#     test4()
#     print 'hw'
#     pass
























