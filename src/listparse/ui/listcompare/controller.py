from listparse.ui.listcompare.view import ListCompareView
from listparse.ui.listcompare.model import ListCompareModel


class ListCompareController:
    model = None
    view = None

    def __init__(self, view=None, model=None):
        if view is None:
            self.view = ListCompareView()
        else:
            self.view = view
        if model is None:
            self.model = ListCompareModel(self.view)
        else:
            self.model = model

        self.bind_handlers()

        if view is None:
            self.view.root.protocol('WM_DELETE_WINDOW', self.close_handler)
            self.view.root.mainloop()

    def bind_handlers(self):
        up_button = self.view.buttons['up']
        up_button.bind("<Button-1>", self.up_handler)

        down_button = self.view.buttons['down']
        down_button.bind("<Button-1>", self.down_handler)

        list_button = self.view.buttons['list']
        list_button.bind("<Button-1>", self.list_handler)

        add_button = self.view.buttons['add']
        add_button.bind("<Button-1>", self.add_handler)

        del_button = self.view.buttons['del']
        del_button.bind("<Button-1>", self.del_handler)

        reload_button = self.view.buttons['reload']
        reload_button.bind("<Button-1>", self.reload_handler)

#        print self.view.radiobuttons
        sort_name_radiobutton = self.view.radiobuttons['name']
        sort_name_radiobutton.bind("<Button-1>", self.result_sort_handler_name)
        sort_year_radiobutton = self.view.radiobuttons['year']
        sort_year_radiobutton.bind("<Button-1>", self.result_sort_handler_year)

    def up_handler(self, event):
        print('up handler')
        self.model.up_selected()

    def down_handler(self, event):
        print('down handler')
        self.model.down_selected()

    def list_handler(self, event):
        print('list handler')
        self.model.list_compare()

    def add_handler(self, event):
        print('add handler')
        self.model.add_list()

    def del_handler(self, event):
        print('del handler')
        self.model.del_list()

    def reload_handler(self, event):
        print('reload handler')
        self.model.reload_lists()

    def result_sort_handler_name(self, event):
        print('result sort handler name')
        self.model.result_sort_change('name')

    def result_sort_handler_year(self, event):
        print('result sort handler year')
        self.model.result_sort_change('year')

    def close_handler(self):
        print('close')
        self.view.close()
