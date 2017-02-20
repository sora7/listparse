'''
Created on 15.03.2014

@author: alex
'''

import HTMLParser
import re
import base64

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

###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

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
#                 pass_link()
                self.ani_link = attrs['href']
                
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
    
        
if __name__ == '__main__':
    pass
    test()
    # test3()
    # test1()
#    test4()
#     print 'hw'
#     pass
























