'''
Created on 24.05.2014

@author: alex
'''

import StringIO
import contextlib

from listparse.parsers.common import AniList, listtype

from listparse.parsers.anidb import Person as AniDBPersonParser
from listparse.parsers.anidb import Company as AniDBCompanyParser
from listparse.parsers.anidb import Mylist as AniDBMylistParser

from listparse.parsers.anidb import TypeList as AniDBListTypeParser
from listparse.parsers.anidb import TypeMylist as AniDBMylistTypeParser

class ListParser(object):
# #    todo:
# #    CSV/XML export/import

    def __init__(self):
        pass

    def parse(self):
        pass

    def person(self):
        pass

    def company(self):
        pass

    def mylist(self):
        pass
        
    def list_check(self, list_file):
        with open(list_file) as f:
            fh = StringIO.StringIO()
            fh.write(f.read())
            info = self.list_check4(fh)
        return info
    
    def list_check4(self, list_fh):
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
    
    def list_person(self, list_file):
    #     titles = None
        with open(list_file) as f:
            fh = StringIO.StringIO()
            fh.write(f.read())
            titles = self.list_person4(fh)
        return titles    

    def list_person4(self, html_fh):
        html_text = html_fh.getvalue()
        
        table_parser = AniDBPersonParser()
        table_parser.feed(html_text.decode('utf-8'))
        titles = table_parser.titles
        print 'list_person', len(titles)
        
        return titles
    
    def list_company(self, list_file):
    #     titles = None
        with open(list_file) as f:
            fh = StringIO.StringIO()
            fh.write(f.read())
            titles = self.list_company4(fh)
        return titles
        
    def list_company4(self, html_fh):
        html_text = html_fh.getvalue()
        
        company_parser = AniDBCompanyParser()
        company_parser.feed(html_text.decode('utf-8'))
        titles = company_parser.titles
        print 'list_company', len(titles)
        
        return titles
    
    
    def list_mylist(self, list_file, completed=False):
        with open(list_file) as f:
            fh = StringIO.StringIO()
            fh.write(f.read())
            titles = self.list_mylist4(fh, completed)
        return titles

    def list_mylist4(self, xml_fh, completed=False):
        xml_text = xml_fh.getvalue()
        mylistParser = AniDBMylistParser()
        mylistParser.feed(xml_text)
        
        titles = mylistParser.titles
        return titles 
    
    @staticmethod
    def print_list(self, lst, uniq=True, field='year'):
        count = 0
        uniq_list = []
        
        for item in sorted(lst, key=lambda i : i.year):
            conditions = []
            data = (item.year, item.ani_name)
            if uniq:
                if data not in uniq_list:
                    uniq_list.append(data)
                    conditions.append(True)
                else:
                    conditions.append(False)
            if not False in conditions:
                print '%s %s' % (data[0], data[1])
                count += 1
        print
        print 'count:', count

class ListCompare(object):

# #    todo
# #    some cute methods like:
# #    union(list1).union(list2).union(list3).diff(list4).inter(list5)
    
    def add(self, initial_list):
        pass

    @staticmethod
    def mk_store(lists):
        # make dict (item.ani_id, item)
        pass

    @staticmethod
    def inter(lists):
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

    @staticmethod
    def diff(lists):
        # titles are in first list, but not in second
        if len(lists) != 2:
            raise ValueError('must be 2 lists')

        list1_set = set([item.ani_id for item in lists[0]])
        list2_set = set([item.ani_id for item in lists[1]])
        differ = list1_set.difference(list2_set)
        
        output = []
        for item in lists[0]:
            if item.ani_id in differ:
                output.append(item)
                
        return output

    @staticmethod
    def union(lists):
        res = []
        for lst in lists:
            for item in lst:
                res.append(item)
        return res

@contextlib.contextmanager
def locked(lock):
    lock.acquire()
    try:
        yield
    finally:
        lock.release() 