'''
Created on 24.05.2014

@author: alex
'''

class ListCompareController:
    model = None
    view = None

    def __init__(self, view, model, standalone=False):
        self.view = view
        self.model = model
        
        self.bind_handlers()

        if standalone:
            # standalone
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

        completed_checkbutton = self.view.checkbuttons['completed']
        completed_checkbutton.bind("<Button-1>", self.result_mode_change_handler)

        aw_listbox = self.view.listboxes['awailable']
        aw_listbox.bind("<Double-Button-1>", self.aw_listbox_doubleclick)

        sel_listbox = self.view.listboxes['selected']
        sel_listbox.bind("<Double-Button-1>", self.sel_listbox_doubleclick)

    def up_handler(self, event):
        print 'up handler'
        self.model.upSelected()

    def down_handler(self, event):
        print 'down handler'
        self.model.downSelected()

    def list_handler(self, event):
        print 'list handler'
        # self.model.listCompare()
        self.model.list_compare()

    def add_handler(self, event):
        print 'add handler'
        self.model.addList()

    def del_handler(self, event):
        print 'del handler'
        self.model.delList()

    def reload_handler(self, event):
        print 'reload handler'
        # self.model.reloadLists()
        self.model.reload_lists()

    def result_sort_handler_name(self, event):
        print 'result sort handler name'
        self.model.resultSortChange('name')

    def result_sort_handler_year(self, event):
        print 'result sort handler year'
        self.model.resultSortChange('year')

    def result_mode_change_handler(self, event):
        print 'result completed handler'
        mode_real = self.view.modes['completed'].get()
        mode_fake = int(not bool(mode_real))
        self.model.resultModeChange(mode_fake)

    def aw_listbox_doubleclick(self, event):
        self.add_handler(event)

    def sel_listbox_doubleclick(self, event):
        self.del_handler(event)

    def close_handler(self):
#         print 'close'
        self.view.close()