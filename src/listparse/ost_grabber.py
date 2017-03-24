import re
import os
import threading

from listparse.loader import Loader

TESHI_DOMAIN = 'http://tenshi.spb.ru'


class OSTGrabber(object):
    __save_path = None

    __titles = None

    __load_titles = None

    __load_files = None
    __curr_file = None

    __loader = None

    __log_cb = None
    __upd_cb = None

    def __init__(self):
        self.__save_path = ''

        self.__titles = []
        self.__load_titles = []

        self.__load_files = []
        self.__curr_file = 0

        self.__loader = Loader()

    def set_log(self, log_function_cb):
        self.__log_cb = log_function_cb

    def set_upd_callback(self, update_callback):
        self.__upd_cb = update_callback

    @property
    def save_path(self):
        return self.__save_path

    @save_path.setter
    def save_path(self, value):
        self.__save_path = value

    @property
    def titles(self):
        return self.__titles

    @property
    def load_titles(self):
        return self.__load_titles

    @property
    def curr_file(self):
        return self.__curr_file

    @property
    def files_count(self):
        return len(self.__load_files)

    def reload_titles(self):
        ost_list_page = TESHI_DOMAIN + '/anime-ost/'

        html_text = self.__loader.get_html(ost_list_page)
# <img src="/icons/folder.gif" alt="[DIR]"> <a href="Angel_Beats/">Angel_Beats/</a>
        rx_ost_dir = re.compile(
            '<img src=["]/icons/folder[.]gif["] alt=["]\[DIR\]["]> '
            '<a href=["](.*)/["]>.*/</a>'
        )

        self.__titles = rx_ost_dir.findall(html_text)
        # print(self.__titles)

    def load(self):
        for title in self.__load_titles:
            url = TESHI_DOMAIN + '/anime-ost/' + title + '/'
            dir_ = title
            self.__log_cb('Processing directories')
            self.__process_dir(url, dir_)

        self.__download_t()

    def __check_n_make(self, dir_path):
        dir_path_full = os.path.join(self.__save_path, dir_path)
        if os.path.exists(dir_path_full):
            if os.path.isdir(dir_path_full):
                pass
            else:
                pass
        else:
            os.mkdir(dir_path_full)

    def __add_file(self, item, dir_url, dir_path):
        file = dict()
        file['url'] = dir_url + item
        filename = item.replace('%20', ' ')
        file['path'] = os.path.join(self.__save_path, dir_path, filename)
        self.__load_files.append(file)

    def __process_dir(self, dir_url, dir_path):
        self.__log_cb('URL: %s' % dir_url)
        self.__log_cb('DIR: %s' % dir_path)

        self.__check_n_make(dir_path)
        html_text = self.__loader.get_html(dir_url)

        # '<a href="Insert_Song_Album.Keep_The_Beats/">'
        rx_dir = re.compile('<a href=["](.*?)["]>')

        items = rx_dir.findall(html_text)[1:]

        rx_item_file = re.compile('.*[.][a-z0-9]{3,4}$')

        rx_item_dir = re.compile('.*/')

            # if item.endswith('.mp3'):
            #     self.__add_file(item, dir_url, dir_path)
            # elif item.endswith('.jpg'):
            #     self.__add_file(item, dir_url, dir_path)
            # elif item.endswith('/'):

        for item in items:
            if bool(rx_item_file.match(item)):
                # item is a file
                self.__add_file(item, dir_url, dir_path)
            elif bool(rx_item_dir.match(item)):
                # item is a dir
                new_dir_url = dir_url + item
                new_dir_path = os.path.join(dir_path, item[:-1])
                self.__process_dir(new_dir_url, new_dir_path)

    def __download(self):
        total = len(self.__load_files)

        for file in self.__load_files:
            self.__curr_file += 1
            self.__upd_cb()
            self.__log_cb('FILE # %s of %s %s' % (self.__curr_file,
                                                  total,
                                                  file['url']))

            file_bin = self.__loader.get_file(file['url'])
            with open(file['path'], 'wb') as f:
                f.write(file_bin)

            self.__log_cb('DONE: %s' % file['path'])

    def __download_t(self):
        t = threading.Thread(target=self.__download)
        t.start()
