import tkinter

from listparse.compare import ListLoader, ListComparator

LISTS_DIR = '../LISTS'

class ListCompareModel:
    view = None

    list_loader = None
    list_comparator = None

    def __init__(self, view_):
        self.view = view_

        self.list_loader = ListLoader()
        self.list_comparator = ListComparator()

    def up_selected(self):
        print('UP')
        selected = self.list_comparator.lists
        listbox = self.view.listboxes['selected']

        indexes = list(map(int, listbox.curselection()))
        print('old', indexes)
        new = [i for i in indexes]
        for i in indexes:
            if i != indexes.index(i):
                selected[i], selected[i-1] = selected[i-1], selected[i]
                new[indexes.index(i)] -= 1
        self.display_selected()

    def down_selected(self):
        print('DOWN')
        selected = self.list_comparator.lists
        listbox = self.view.listboxes['selected']

        indexes = sorted(map(int, listbox.curselection()), reverse=True)
        print('old', indexes)
        new = [i for i in indexes]
        for i in indexes:
            if i != listbox.size() - indexes.index(i) - 1:
                selected[i], selected[i+1] = selected[i+1], selected[i]
                new[indexes.index(i)] += 1
        self.display_selected()

    def list_compare(self):
        mode = self.view.modes['list_compare'].get()
        self.list_comparator.compare(mode)

        self.uniq_result()
        self.sort_result()
        self.display_result()

    def add_list(self):
        print('ADD')
        listbox = self.view.listboxes['available']
        indexes = list(map(int, listbox.curselection()))
        indexes.sort(reverse=True)

        available = self.list_loader.lists
        selected = self.list_comparator.lists

        for i in indexes:
            selected.append(available.pop(i))

        self.sort_available()
        self.display_available()
        self.display_selected()

    def del_list(self):
        print('DEL')
        listbox = self.view.listboxes['selected']
        indexes = list(map(int, listbox.curselection()))
        indexes.sort(reverse=True)

        available = self.list_loader.lists
        selected = self.list_comparator.lists

        for i in indexes:
            available.append(selected.pop(i))

        self.sort_available()
        self.display_available()
        self.display_selected()

    def reload_lists(self):
        self.list_loader.reload_lists(LISTS_DIR, self.display_available)
        self.sort_available()
        self.display_available()

    def sort_available(self):
        self.list_loader.lists.sort(
            key=lambda item: (int(item.type), item.name)
        )

    def display_available(self):
        lst = [item.name for item in self.list_loader.lists]
        self.view.display_listbox(self.view.listboxes['available'],
                                  lst,
                                  self.view.textlabels['available_stat']
                                  )

    def display_selected(self):
        lst = [item.name for item in self.list_comparator.lists]
        self.view.display_listbox(self.view.listboxes['selected'],
                                  lst,
                                  self.view.textlabels['selected_stat']
                                  )

    def sort_result(self):
        mode = self.view.modes['result_sort'].get()
        print(mode)
        if mode == 'year':
            function = lambda item: (item.year, item.ani_name)
        elif mode == 'name':
            function = lambda item: (item.ani_name, item.year)

        self.list_comparator.result.sort(key=function)

    def uniq_result(self):
        result = self.list_comparator.result
        uniq_dict = dict(
            (item.ani_id, item) for item in result
            )
        result[:] = uniq_dict.values()

    def display_result(self):
        inp_list = self.list_comparator.result
        res_list = ['%s %s' % (item.year, item.ani_name) for item in inp_list]
        self.view.display_listbox(self.view.listboxes['result'],
                                  res_list,
                                  self.view.textlabels['result_stat']
                                  )

    def result_sort_change(self, type_):
        self.view.modes['result_sort'].set(type_)
        self.sort_result()
        self.display_result()
