from time import gmtime, strftime
from tkinter.filedialog import askdirectory
import os

from listparse.ost_grabber import OSTGrabber

OST_DIR_DEFAULT = 'ost'


class TenshiOstModel(object):
    view = None

    __grabber = None

    def __init__(self, view_):
        self.view = view_

        self.__grabber = OSTGrabber()
        self.__grabber.save_path = OST_DIR_DEFAULT
        self.__grabber.set_log(self.log)
        self.__grabber.set_upd_callback(self.upd_progress)

    def savepath_change(self):
        ost_dir = askdirectory(parent=self.view.root, initialdir=os.getcwd(),
                               title='Select a directory to save OSTs')
        print(ost_dir)
        self.__grabber.save_path = ost_dir

    def reload(self):
        print('reload')
        self.__grabber.reload_titles()
        self.display_available()

    def add_titles(self):
        print('ADD')
        listbox = self.view.listboxes['available']
        indexes = list(map(int, listbox.curselection()))
        indexes.sort(reverse=True)

        available = self.__grabber.titles
        selected = self.__grabber.load_titles

        for i in indexes:
            selected.append(available.pop(i))

        self.__grabber.titles.sort()

        self.display_available()
        self.display_selected()

    def del_titles(self):
        print('DEL')
        listbox = self.view.listboxes['selected']
        indexes = list(map(int, listbox.curselection()))
        indexes.sort(reverse=True)

        available = self.__grabber.titles
        selected = self.__grabber.load_titles

        for i in indexes:
            available.append(selected.pop(i))

        self.__grabber.titles.sort()

        self.display_available()
        self.display_selected()

    def load(self):
        self.__grabber.load()

    def display_available(self):
        lst = self.__grabber.titles
        self.view.display_listbox(self.view.listboxes['available'], lst)

    def display_selected(self):
        lst = self.__grabber.load_titles
        self.view.display_listbox(self.view.listboxes['selected'], lst)

    def log(self, message):
        print(message)
        text = '[%s] %s'%(strftime("%Y.%m.%d %H:%M:%S", gmtime()), message)
        self.view.log_add(text)

    def upd_progress(self):
        total = self.__grabber.files_count
        curr = self.__grabber.curr_file

        self.view.progress['maximum'] = total
        self.view.progress['value'] = curr

        self.view.textlabels['progress'].set(int(curr / total * 100))
