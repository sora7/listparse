import re

from listparse.loader import Loader

TESHI_DOMAIN = 'http://tenshi.spb.ru'


class OSTGrabber(object):
    __save_path = None
    __titles = None

    __loader = None

    def __init__(self):
        self.__save_path = ''
        self.__titles = []

        self.__loader = Loader()

    @property
    def save_path(self):
        return self.__save_path

    @save_path.setter
    def save_path(self, value):
        self.__save_path = value

    @property
    def titles(self):
        return self.__titles

    def fetch_titles(self):
        titles = []

        ost_list_page = TESHI_DOMAIN + '/anime-ost/'



        self.__titles = titles
