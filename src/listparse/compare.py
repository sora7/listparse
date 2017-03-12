import os

from listparse.ui.listcompare.common import listtype, locked, ListParser, ListCompare


class CompareMode(object):
    INTERSECT = 1
    UNION = 2
    DIFFER = 3


compare_mode = CompareMode()


class ListComparator(object):

    def __init__(self):
        mode = compare_mode.INTERSECT
        pass

    def intersect(self, lists):
        pass


class ListLoader(object):
    __lists = None
    __listParser = None

    def __init__(self):
        self.__lists = []
        self.__listParser = ListParser()

    @property
    def lists(self):
        return self.__lists

    def reload_lists(self, lists_path, cb_add_one=None):
        self.lists[:] = []
        for list_file in os.listdir(lists_path):
            list_file_fullpath = os.path.join(lists_path, list_file)
            lst = self.__listParser.list_check(list_file_fullpath)
            if lst.type != listtype.UNKNOWN:
                lst.path = list_file_fullpath
                self.__lists.append(lst)
                if cb_add_one is not None:
                    cb_add_one()


