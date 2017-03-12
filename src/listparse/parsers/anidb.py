import html.parser as HTMLParser
import re
import base64
from functools import reduce

from listparse.parsers.common import AniTitle, AniList, Dict, Bool, pass_year, listtype, StopPleaseException


class Person(HTMLParser.HTMLParser):
    is_table = False
    is_row = False
    is_col = False

    CHAR_LINK = 'http://anidb.net/perl-bin/animedb.pl\?show=character&charid='
    CHAR_LINK_PATTERN = re.compile(CHAR_LINK + '(\d+)')
    ANI_LINK = 'http://anidb.net/perl-bin/animedb.pl\?show=anime&aid='
    ANI_LINK_PATTERN = re.compile(ANI_LINK + '(\d+)')

    __titles = None

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
        self.__titles = []
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
                    self.__titles.append(title)
    @property
    def titles(self):
        return self.__titles


class Company(HTMLParser.HTMLParser):
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
    _type = None
    eps = None
    year = None
    credit = None

    ANI_LINK = 'http://anidb.net/perl-bin/animedb.pl\?show=anime&aid='
    ANI_LINK_PATTERN = re.compile(ANI_LINK + '(\d+)')

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
                    link = attrs['href']
                    if self.ANI_LINK_PATTERN.match(link):
                        self.ani_id = self.ANI_LINK_PATTERN.findall(link)[0]
                        self.ani_link = link
                        # print self.ani_link, self.ani_id
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
                        self._type = data
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
                # print self.ani_id
                title.ani_link = self.ani_link
                pass_year(title, str(self.year))

                title.type = self._type
                self.__animes.append(title)

    @property
    def titles(self):
        return self.__animes


class Mylist(HTMLParser.HTMLParser):
    is_animes = False
    is_ani = False
    is_titles = False
    is_title = False

    __animes = []

    ani_id = None
    _type = None
    year = None
    completed = None
    ani_date_start = None
    ani_date_end = None
    eps = None
    s_eps = None
    ani_name = None

    def purge(self):
        self.ani_id = None
        self._type = None
        self.year = None
        self.completed = None
        self.ani_date_start = None
        self.ani_date_end = None
        self.eps = None
        self.s_eps = None
        self.ani_name = None

    def is_empty(self):
        return (self.ani_id == None and
                self._type == None and
                self.year == None and
                self.completed == None and
                self.ani_date_start == None and
                self.ani_date_end == None and
                self.eps == None and
                self.s_eps == None and
                self.ani_name == None
                )

    def process_cdata(self, text):
        '''
        get the fuck out all cdata
        encode them by base64
        '''
        def process1(text):
            # bad
            data = text
            data = data.replace('<![CDATA[', '"').replace(']]>', '"')
            return data

        def process2(text):
            # very slow
            cdata_regexp = re.compile(r'<!\[CDATA\[?(.+?)\]\]>')
            while re.search(cdata_regexp, text) is not None:
                # print s
                found_cdata = re.search(cdata_regexp, text).group()
                name = re.search(cdata_regexp, text).group(1).strip()
                name_coded = base64.b64encode(name)
                text = text.replace(found_cdata, name_coded)
            return text

        def process3(text):
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

        return process3(text)

    def __init__(self):
        self.is_animes = False
        self.is_ani = False
        self.is_titles = False
        self.is_title = False

        self.purge()
        self.__animes = []
        HTMLParser.HTMLParser.__init__(self)

    def feed(self, data):
        data = self.process_cdata(data)
        HTMLParser.HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        if tag == 'animes':
            self.is_animes = True

        if self.is_animes:
            attrs = Dict(attrs)
            if tag == 'anime':
                self.is_ani = True

                self.ani_id = str(attrs['id'])
                self._type = str(attrs['type'])
                self.year = str(attrs['year'])
            if tag == 'status':
                if str(attrs['watched']) == '1':
                    self.completed = True
                else:
                    self.completed = False

            if tag == 'neps':
                self.eps = attrs['cnt']
            if tag == 'seps':
                self.s_eps = attrs['cnt']

            if tag == 'titles':
                self.is_titles = True

            if self.is_titles:
                if tag == 'title':
                    if attrs['type'] == 'main':
                        self.is_title = True
            if tag == 'dates':
                self.ani_date_start = attrs['start']
                self.ani_date_end = attrs['end']

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
                    if self.is_title:
                        self.ani_name = base64.b64decode(data)
            else:
                if not self.is_empty():
                    # print self.ani_id, self.ani_name
                    ani = AniTitle()
                    ani.ani_id = self.ani_id
                    ani.ani_name = self.ani_name
                    ani.type = self._type
                    pass_year(ani, self.year)
                    ani.completed = self.completed
                    ani.eps = self.eps
                    ani.s_eps = self.s_eps
                    ani.date_start = self.ani_date_start
                    ani.date_end = self.ani_date_end
                    self.__animes.append(ani)
                    self.purge()

    @property
    def titles(self):
        return self.__animes

class TypeTitle(object):
    pass

class TypeList(HTMLParser.HTMLParser):
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
            if self.is_person:
                lst.type = listtype.PERSON
            if self.is_company:
                lst.type = listtype.COMPANY
        else:
            lst.type = listtype.UNKNOWN
        return lst

class TypeMylist(HTMLParser.HTMLParser):
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
            print('MUYLIST PARSER LOL=====================>>')
            lst.type = listtype.MYLIST
            lst.name = 'mylist'
        else:
            lst.type = listtype.UNKNOWN
        return lst
