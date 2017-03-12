'''
Created on 24.05.2014

@author: alex
'''

import threading
import platform
import os

from common import listtype, locked, ListParser, ListCompare

class ListCompareModel:
    view = None

    reload_lock = None
    compare_lock = None

    lists = {}

    def __init__(self, view_):
        self.view = view_
        
        self.lists['result'] = []
        self.lists['selected'] = []
        self.lists['awailable'] = []
        
        self.reload_lock = threading.Lock()
        self.compare_lock = threading.Lock()
        
    def upSelected(self):
        print 'UP'
        listbox = self.view.listboxes['selected']
        selected = self.lists['selected']
        
        indexes = map(int, listbox.curselection())
        print 'old', indexes
        new = [i for i in indexes]
        for i in indexes:
            if i != indexes.index(i):
                selected[i], selected[i - 1] = selected[i - 1], selected[i]
                new[indexes.index(i)] -= 1
        print 'new'
        
        self.displaySelected()

    def downSelected(self):
        print 'DOWN'
        selected = self.lists['selected']
        listbox = self.view.listboxes['selected']
        
        indexes = sorted(map(int, listbox.curselection()), reverse=True)
        print 'old', indexes
        new = [i for i in indexes]
        for i in indexes:
            if i != listbox.size() - indexes.index(i) - 1:
                selected[i], selected[i + 1] = selected[i + 1], selected[i]
                new[indexes.index(i)] += 1
        print 'new', new
        self.displaySelected()

    def list_compare(self):
        def thread_task():
            with locked(self.compare_lock):
                self.listCompare()

        if platform.system() == 'Windows':
            thread_task()
        else:
            if not self.compare_lock.locked():
                t1 = threading.Thread(target=thread_task)
                t1.start()
                print "THREAD START"
                t1.join(0.1)

    def listCompare(self):
        print 'LIST COMPARE'
        selected = self.lists['selected']
        result = self.lists['result']
        
        lists = []
        parser = ListParser()
        for item in selected:
# #            try:
# #                lists.append(parser.parse(item))
# #            except ValueError:
# #                pass
            if item.type != listtype.UNKNOWN:
                if item.type == listtype.PERSON:
                    lst = parser.list_person(item.path)
                elif item.type == listtype.COMPANY:
                    lst = parser.list_company(item.path)
                elif item.type == listtype.MYLIST:
                    lst = parser.list_mylist(item.path)
                    
                lists.append(lst)
        res = []
        compare = ListCompare
        compareMode = self.view.modes['list_compare'].get()
        if compareMode == 'intersect':
            res = compare.inter(lists)
        elif compareMode == 'differ':
            res = compare.diff(lists[0:2])
        elif compareMode == 'union':
            res = compare.union(lists)
        print 'LENGTH', len(res)
        result[:] = res
        
        self.uniqResult()
        self.sortResult()
        self.displayResult()

    def addList(self):
        print 'ADD'
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
        print 'ADD'
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
        def thread_task():
            with locked(self.reload_lock):
                self.reloadLists()

        if platform.system() == 'Windows':
            thread_task()
        else:
            if not self.reload_lock.locked():
                t1 = threading.Thread(target=thread_task)
                t1.start()
                print "THREAD START"
                t1.join(0.1)

    def reloadLists(self):
        join = os.path.join
        listdir = os.listdir
        isfile = os.path.isfile
#         abspath = os.path.abspath
        
        print 'RELOAD'        
#         LISTS_DIR = 'lists'
#         curdir = abspath(os.path.curdir)
#         LISTS_PATH = os.path.normpath(join(curdir, LISTS_DIR))
        #LISTS_PATH = os.path.normpath("/home/alex/prog/workspace/CertainProg/lists/")
        LISTS_PATH = os.path.normpath("../../../lists/")
        print LISTS_PATH
        
        awailable = self.lists['awailable']
        awailable[:] = []
        selected = self.lists['selected']
        selected[:] = []
        self.displaySelected()

        parser = ListParser()

        dir_items = map(lambda x: join(LISTS_PATH, x), listdir(LISTS_PATH))
        dir_files = filter(lambda item: isfile(item), dir_items)
        for list_file in dir_files:
            lst = parser.list_check(list_file)
            if lst.type != listtype.UNKNOWN:
                lst.path = list_file
                print lst.type, lst.name
                awailable.append(lst)
                self.sortAwailable()
                self.displayAwailable()
#            self.view.buttons['reload'].flash()

    def sortAwailable(self):
        lst = self.lists['awailable']
        lst.sort(key=lambda item : (item.type, item.name))

    def displayAwailable(self):
        self.view.display_awailable(self.lists['awailable'])

    def displaySelected(self):
        self.view.display_selected(self.lists['selected'])

    def sortResult(self):
        mode = self.view.modes['result_sort'].get()
        print mode
        if mode == 'year':
            function = lambda item : (item.year, item.ani_name)
        elif mode == 'name':
            function = lambda item : (item.ani_name, item.year)
        self.lists['result'].sort(key=function)

    def uniqResult(self):
        result = self.lists['result']
        uniq_dict = dict(
            (item.ani_id, item) for item in result
            )
        result[:] = uniq_dict.values()

    def displayResult(self, mode_fake=None):
        result = []
        result[:] = self.lists['result']
        
        if mode_fake == None:
            completed = bool(self.view.modes['completed'].get())
        else:
            completed = bool(mode_fake)
        print 'COMPLETED:', completed
        if completed:
            result = filter(lambda item: item.completed, result)
        
        self.view.display_result(result)

    def resultModeChange(self, mode_fake):
        self.displayResult(mode_fake=mode_fake)

    def resultSortChange(self, type_):
        self.view.modes['result_sort'].set(type_)
        self.sortResult()
        self.displayResult() 