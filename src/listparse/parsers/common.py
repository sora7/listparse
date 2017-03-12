import re
from enum import Enum

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


class StopPleaseException(Exception):

    def __init__(self):
        pass


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
        if key in self.__store:
            return self.__store[key]
        else:
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


# class LISTTYPE(object):
#     @staticmethod
#     @property
#     def UNKNOWN(self):
#         return 0
#
#     @staticmethod
#     @property
#     def PERSON(self):
#         return 1
#
#     @staticmethod
#     @property
#     def COMPANY(self):
#         return 2
#
#     @staticmethod
#     @property
#     def MYLIST(self):
#         return 3


class LISTTYPE(object):
    UNKNOWN = 0
    PERSON = 1
    COMPANY = 2
    MYLIST = 3

listtype = LISTTYPE()

# class listtype(Enum):
#     UNKNOWN = 0
#     PERSON = 1
#     COMPANY = 2
#     MYLIST = 3


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

    def __str__(self):
        return 'type: %s, name: %s, path: %s' %(self.__type,
                                                self.__name,
                                                self.__path)

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
        self.__list = value

