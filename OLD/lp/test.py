import os
import HTMLParser
import re

def conv(inp_str):
    try:
        return str(inp_str)
    except UnicodeEncodeError:
        try:
            return ''.join(chr(char) for char in inp_str)
        except TypeError:
            #return inp_str
            return None

class Dict():
    store = None
    
    def __init__(self, input_lst):
        self.store = dict()
        
        for (key, value) in input_lst:
            self.store[conv(key)] = conv(value)
    
    def __getitem__(self, key):
        if self.store.has_key(key):
            return self.store[key]
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
                            
                            print 'char id:', self.char_id
                            self.title['char_id'] = str(self.char_id)
                            print 'char link:', self.char_link
                            self.title['char_link'] = str(self.char_link)
                            print 'char namae2:', self.char_name
                            self.title['char_name'] = self.char_name
                            print 'ani id:', self.ani_id
                            self.title['ani_id'] = str(self.ani_id)
                            print 'ani link:', self.ani_link
                            self.title['ani_link'] = str(self.ani_link)
                            print 'ani namae:', data
                            self.title['ani_name'] = data
                            
                            self.is_ani = False
                    if self.is_type:
                        self.title['type'] = str(data)
                        print 'type:', data
                        self.is_type = False
                    if self.is_eps:
                        self.title['eps'] = str(data)
                        print 'eps:', data
                        self.is_eps = False
                    if self.is_year:
                        self.title['year'] = str(data)
                        print 'year:', data
                        self.is_year = False
                        print '##########################################'
#                    self.rowdata.append(data)
            else:
                #self.tabledata.append(self.rowdata)
                #self.rowdata = []
                if len(self.title) != 0:
                    self.titles.append(self.title)
                self.title = {}

    def get_info(self):
        pass

    def get_titles(self):
        #return self.tabledata
        return self.titles
        #return self.tables
        #return self.rowdata
        #return self.c


url = 'http://ru.wikipedia.org/wiki/%D0%91%D1%80%D0%B0%D1%83%D0%B7%D0%B5%D1%80'
#print url

#html_text = ''.join(urllib.urlopen(url).readlines())
#print html_text
curdir =  os.path.abspath(os.path.curdir)
file_ = '  AniDB.net   Person - Hanazawa Kana   .html'
file_path = os.path.join(curdir, 'lists', file_)
with open(file_path) as f:
    html_text = ''.join(f.readlines())
    table_parser = PersonParser()
    table_parser.feed(html_text.decode('utf-8'))
    titles = table_parser.get_titles()
    #print table_parser.get_tables()
    #print len(table_parser.get_tables())
for t in titles:
    print t
    
