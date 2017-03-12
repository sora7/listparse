import os
import tkinter

from listparse.ui.listcompare.common import listtype, locked, ListParser, ListCompare

from listparse.compare import ListLoader


class ListCompareModel:
    view = None

    list_loader = None

    lists = {}

    def __init__(self, view_):
        self.view = view_

        self.list_loader = ListLoader()

        self.lists['result'] = []
        self.lists['selected'] = []
        self.lists['awailable'] = []

    def upSelected(self):
        print('UP')
        selected = self.lists['selected']
        listbox = self.view.listboxes['selected']

        indexes = map(int, listbox.curselection())
        print('old', indexes)
        new = [i for i in indexes]
        for i in indexes:
            if i != indexes.index(i):
                selected[i], selected[i-1] = selected[i-1], selected[i]
                new[indexes.index(i)] -= 1
        print('new')
        self.displaySelected()

    def downSelected(self):
        print('DOWN')
        selected = self.lists['selected']
        listbox = self.view.listboxes['selected']

        indexes = sorted(map(int, listbox.curselection()), reverse=True)
        print('old', indexes)
        new = [i for i in indexes]
        for i in indexes:
            if i != listbox.size() - indexes.index(i) - 1:
                selected[i], selected[i+1] = selected[i+1], selected[i]
                new[indexes.index(i)] += 1
        print('new', new)
        self.displaySelected()

    def listCompare(self):
        print('LIST COMPARE')
        selected = self.lists['selected']
        result = self.lists['result']

        # lists = []
        # for item in selected:
        #     if item.type != listtype.UNKNOWN:
        #         if item.type == listtype.PERSON:
        #             lst = list_person(item.path)
        #         elif item.type == listtype.COMPANY:
        #             lst = list_company(item.path)
        #         elif item.type == listtype.MYLIST:
        #             lst = list_mylist(item.path)
        #         lists.append(lst)
        # res = []
        # compareMode = self.view.modes['list_compare'].get()
        # if compareMode == 'intersect':
        #     res = list_inter(lists)
        # elif compareMode == 'differ':
        #     res = list_diff(lists[0:2])
        # elif compareMode == 'union':
        #     for lst in lists:
        #         for item in lst:
        #             res.append(item)
        # print 'LENGTH', len(res)
        # result[:] = res

        self.uniqResult()
        self.sortResult()
        self.displayResult()

    def addList(self):
        print('ADD')
        listbox = self.view.listboxes['awailable']
        indexes = map(int, listbox.curselection())
        indexes.sort(reverse=True)
        awailable = self.lists['awailable']
        selected = self.lists['selected']

        for i in indexes:
            selected.append(awailable.pop(i))

        self.sortAwailable()
        self.displayAwailable()
        self.displaySelected()

    def delList(self):
        print('ADD')
        listbox = self.view.listboxes['selected']
        indexes = map(int, listbox.curselection())
        indexes.sort(reverse=True)
        awailable = self.lists['awailable']
        selected = self.lists['selected']

        for i in indexes:
            awailable.append(selected.pop(i))

        self.sortAwailable()
        self.displayAwailable()
        self.displaySelected()

    def reload_lists(self):
        LISTS_DIR = '../lists'
        self.list_loader.reload_lists(LISTS_DIR, self.displayAwailable)
        # self.lists['awailable']
        self.sortAwailable()
        self.displayAwailable()
        # listParser = ListParser()
        # print('RELOAD')
        # LISTS_DIR = '../lists'
        # curdir = os.path.abspath(os.path.curdir)
        # LISTS_PATH = os.path.normpath(os.path.join(curdir, LISTS_DIR))
        # print(LISTS_PATH)
        #
        # awailable = self.lists['awailable']
        #
        # awailable[:] = []
        # for list_file in os.listdir(LISTS_PATH):
        #     list_file_fullpath = os.path.join(LISTS_PATH, list_file)
        #     lst = listParser.list_check(list_file_fullpath)
        #     if lst.type != listtype.UNKNOWN:
        #         lst.path = list_file_fullpath
        #         print('CURR LST: ', lst)
        #         print(lst.type)
        #         awailable.append(lst)
        #         self.sortAwailable()
        #         self.displayAwailable()

    def sortAwailable(self):
        lst = self.lists['awailable']
        lst.sort(key=lambda item: (int(item.type), item.name))

    def displayAwailable(self):
        listbox = self.view.listboxes['awailable']
        textlabel = self.view.textlabels['awailable_stat']
        # awailable = self.lists['awailable']
        awailable = self.list_loader.lists

        listbox.delete(0, tkinter.END)
        for item in awailable:
            listbox.insert(tkinter.END, '%s' % (item.name))
        listbox.update()

        textlabel.set('%d lists awailable' % (len(awailable)))

    def displaySelected(self):
        listbox = self.view.listboxes['selected']
        selected = self.lists['selected']

        listbox.delete(0, tkinter.END)
        for item in selected:
            listbox.insert(tkinter.END, '%s' % (item.name))
        listbox.update()

        #self.sortResult()

    def sortResult(self):
        mode = self.view.modes['result_sort'].get()
        print(mode)
        if mode == 'year':
            function = lambda item: (item.year, item.ani_name)
        elif mode == 'name':
            function = lambda item: (item.ani_name, item.year)
        self.lists['result'].sort(key=function)

    def uniqResult(self):
        result = self.lists['result']
        uniq_dict = dict(
            (item.ani_id, item) for item in result
            )
        result[:] = uniq_dict.values()

    def displayResult(self):
        listbox = self.view.listboxes['result']
        result = self.lists['result']
        textlabel = self.view.textlabels['result_stat']

        listbox.delete(0, tkinter.END)
        for item in result:
            listbox.insert(tkinter.END, '%s %s' % (item.year, item.ani_name))

        textlabel.set('count: %i' % len(result))
        listbox.update()

    def resultSortChange(self, type_):
        self.view.modes['result_sort'].set(type_)
        self.sortResult()
        self.displayResult()
