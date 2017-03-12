from io import StringIO
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
        with open(list_file, encoding='utf-8') as f:
            fh = StringIO()
            fh.write(f.read())
            info = self.list_check4(fh)
        return info

    @staticmethod
    def list_check4(list_fh):
        file_text = list_fh.getvalue()
        aniParser = AniDBListTypeParser()
        aniParser.feed(file_text)
        lst = aniParser.get_type()
        if lst.type == listtype.UNKNOWN:
            lst = AniList()
            print('MUYLIST LISTCHECK LOL=====================>>')
            mylistTypeParser = AniDBMylistTypeParser()
            mylistTypeParser.feed(file_text)
            lst = mylistTypeParser.type
        return lst

    def list_person(self, list_file):
        with open(list_file, encoding='utf-8') as f:
            fh = StringIO()
            fh.write(f.read())
            titles = self.list_person4(fh)
        return titles

    def list_person4(self, html_fh):
        html_text = html_fh.getvalue()

        table_parser = AniDBPersonParser()
        table_parser.feed(html_text)
        titles = table_parser.titles
        print('list_person', len(titles))

        return titles

    def list_company(self, list_file):
    #     titles = None
        with open(list_file, encoding='utf-8') as f:
            fh = StringIO()
            fh.write(f.read())
            titles = self.list_company4(fh)
        return titles

    def list_company4(self, html_fh):
        html_text = html_fh.getvalue()

        company_parser = AniDBCompanyParser()
        company_parser.feed(html_text)
        titles = company_parser.titles
        print('list_company', len(titles))

        return titles


    def list_mylist(self, list_file, completed=False):
        with open(list_file, encoding='utf-8') as f:
            fh = StringIO()
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
                print('%s %s' % (data[0], data[1]))
                count += 1
        print()
        print('count:', count)

@contextlib.contextmanager
def locked(lock):
    lock.acquire()
    try:
        yield
    finally:
        lock.release()


