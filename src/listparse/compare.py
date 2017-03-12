import os

from listparse.ui.listcompare.common import listtype, ListParser


class CompareMode(object):
    INTERSECT = 1
    UNION = 2
    DIFFER = 3

compare_mode = CompareMode()


class ListComparator(object):
    __lists = None
    __result = None

    __listParser = None

    def __init__(self):
        self.__lists = []
        self.__result = []
        self.__listParser = ListParser()

    @property
    def lists(self):
        return self.__lists

    @property
    def result(self):
        return self.__result

    def compare(self, mode):
        lists = []
        for item in self.__lists:
            if item.type != listtype.UNKNOWN:
                if item.type == listtype.PERSON:
                    lst = self.__listParser.list_person(item.path)
                elif item.type == listtype.COMPANY:
                    lst = self.__listParser.list_company(item.path)
                elif item.type == listtype.MYLIST:
                    lst = self.__listParser.list_mylist(item.path)
                lists.append(lst)

        if mode == compare_mode.INTERSECT:
            self.__result = self.intersect_(lists)
        elif mode == compare_mode.DIFFER:
            self.__result = self.differ_(lists)
        elif mode == compare_mode.UNION:
            self.__result = self.union_(lists)

    @staticmethod
    def intersect_(lists):
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
    def differ_(lists):
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
    def union_(lists):
        res = []
        for lst in lists:
            for item in lst:
                res.append(item)
        return res


class ListLoader(object):
    __lists = None
    __listParser = None

    def __init__(self):
        self.__lists = []
        self.__listParser = ListParser()

    @property
    def lists(self):
        return self.__lists

    # cb_add_one - callback function (update view or smtg)
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

