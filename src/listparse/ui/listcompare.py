import tkinter
import tkinter.ttk

FRAME_BORDER = 0

class ListCompareView:
    # main window
    root = None

    listboxes = {}
    buttons = {}
    radiobuttons = {}

    textlabels = {}
    modes = {}

    def close(self):
        self.root.destroy()
        self.root.quit()

    def __init__(self, root=None, main_frame=None):
        self.createWidgets(root, main_frame)

    def createWidgets(self, root, main_frame):
        if root == None:
            # standalone
            self.root = tkinter.Tk()
            self.root.title('List Compare')
            w = 600
            h = 500
            self.root.geometry('%sx%s+0+0' % (w, h))
        else:
            # inside
            self.root = root

        self.modes['result_sort'] = tkinter.StringVar()
        self.modes['result_sort'].set('year')

        self.modes['list_compare'] = tkinter.StringVar()
        self.modes['list_compare'].set('intersect')

        self.textlabels['result_stat'] = tkinter.StringVar()
        self.textlabels['result_stat'].set('count: 0')

        self.textlabels['awailable_stat'] = tkinter.StringVar()
        self.textlabels['awailable_stat'].set('0 lists awailable')

        self.mk_main_frame(main_frame)

    def mk_main_frame(self, main):
        if main == None:
            # standalone
            main_frame = tkinter.Frame(master=self.root, bg='black', bd=FRAME_BORDER)
            main_frame.pack(fill='both', expand=True)
        else:
            # inside
            main_frame = main

        self.mk_result_frame(main_frame)
        self.mk_additional_frame(main_frame)

    def mk_result_frame(self, main_frame):
        result_frame = tkinter.Frame(master=main_frame, bg='red',
                                     bd=FRAME_BORDER)
        result_frame.pack(side='left', fill='both', expand=True)

        tkinter.ttk.Label(result_frame, text='result list').pack(fill='both',
                                                                 side='top')
        self.mk_statistic_frame(result_frame)

        self.listboxes['result'] = tkinter.Listbox(result_frame,
                                                   selectmode=tkinter.EXTENDED)
        result_listbox = self.listboxes['result']
        result_listbox.pack(side='left', fill='both', expand=True)

        res_scrollBar = tkinter.ttk.Scrollbar(result_frame)
        res_scrollBar.pack(side='right', fill='y', expand=False)
        res_scrollBar['command'] = result_listbox.yview
        result_listbox['yscrollcommand'] = res_scrollBar.set

    def mk_statistic_frame(self, result_frame):
        statistic_frame = tkinter.Frame(result_frame, bg='blue',
                                        bd=FRAME_BORDER)
        statistic_frame.pack(side='bottom', fill='both', expand=False)

        sort_label = tkinter.ttk.Label(statistic_frame, text='sort:')
        sort_label.pack(side='left', fill='both')

        res_sort_mode = self.modes['result_sort']

        RADIO = (
            ('name', 'name'),
            ('year', 'year')
            )

        radio_opt = {'side': 'left', 'fill': 'none'}
        for title, value_ in RADIO:
            self.radiobuttons[title] = tkinter.Radiobutton(statistic_frame,
                                text=title,
                                variable=res_sort_mode,
                                value=value_,
                                anchor='w')
            self.radiobuttons[title].pack(**radio_opt)

        exp_label = tkinter.ttk.Label(statistic_frame, text='EXPAND')
        exp_label.pack(side='left', fill='both', expand=True)

        stat_label = tkinter.ttk.Label(statistic_frame,
                                       textvariable=
                                       self.textlabels['result_stat']
                                       )
        stat_label.pack(side='left', fill='both')

    def mk_additional_frame(self, main_frame):
        additinal_frame = tkinter.Frame(master=main_frame,
                                        bg='blue',
                                        bd=FRAME_BORDER
                                        )
        additinal_frame.pack(side='right', fill='both', expand=False)

        self.mk_selected_frame(additinal_frame)
        self.mk_awailable_frame(additinal_frame)

    def mk_selected_frame(self, additional_frame):
        selected_frame = tkinter.Frame(additional_frame,
                                       bg='green',
                                       bd=FRAME_BORDER)
        selected_frame.pack(side='top', fill='both', expand=True)

        selectedLabel = tkinter.ttk.Label(selected_frame, text='selected lists')
        selectedLabel.pack(fill='both')

        self.listboxes['selected'] = tkinter.Listbox(selected_frame,
                                           selectmode=tkinter.EXTENDED)
        sel_listbox = self.listboxes['selected']
        sel_listbox.pack(side='left', fill='both', expand=True)

        sel_scrollBar = tkinter.ttk.Scrollbar(selected_frame)
        sel_scrollBar.pack(side='left', fill='y', expand=False)
        sel_scrollBar['command'] = sel_listbox.yview
        sel_listbox['yscrollcommand'] = sel_scrollBar.set

# #        style = ttk.Style()
# #        style.map('C.TButton',
# #                  foreground=[('pressed','red'),('active','blue')],
# #                  background=[('pressed','!disabled','black'),('active','white')]
# #            )
        BUTTONS = (
            ('UP', 'up'),
            ('DOWN', 'down'),
            ('LIST', 'list'),
            )

        # third button will be expand
        exp = 3
        for title, name in BUTTONS:
            exp -= 1
            self.buttons[name] = tkinter.ttk.Button(selected_frame, text=title)
            self.buttons[name].pack(side='top', fill='both',
                                    expand=not bool(exp))

        mode_label = tkinter.ttk.Label(selected_frame, text='mode:', anchor='n')
        mode_label.pack(side='top', fill='x')

        compare_mode = self.modes['list_compare']

        RADIO = (
            ('intersect', 'intersect'),
            ('differ',    'differ'),
            ('union',     'union')
            )

        radio_opt = {'side': 'top', 'fill': 'x'}
        for title, value_ in RADIO:
            tkinter.Radiobutton(selected_frame, text=title,
                                variable=compare_mode, value=value_,
                                anchor='w').pack(**radio_opt)

    def mk_awailable_frame(self, additinal_frame):
        awailable_frame = tkinter.Frame(additinal_frame,
                                        bg='red',
                                        bd=FRAME_BORDER)
        awailable_frame.pack(side='top', fill='both', expand=True)

        self.mk_aw_buttons_frame(awailable_frame)

        aw_label = tkinter.ttk.Label(awailable_frame, text='awailable lists')
        aw_label.pack(side='top',fill='both')

        stat_label = tkinter.ttk.Label(awailable_frame,
                            textvariable=self.textlabels['awailable_stat'])
        stat_label.pack(side='bottom', fill='both')

        self.listboxes['awailable'] = tkinter.Listbox(awailable_frame,
                                                      selectmode=
                                                      tkinter.EXTENDED)

        aw_listbox = self.listboxes['awailable']
        aw_listbox.pack(side='left', fill='both', expand=True)
        aw_scrollBar = tkinter.ttk.Scrollbar(awailable_frame)
        aw_scrollBar.pack(side='right', fill='y', expand=False)
        aw_scrollBar['command'] = aw_listbox.yview
        aw_listbox['yscrollcommand'] = aw_scrollBar.set

    def mk_aw_buttons_frame(self, awailable_frame):
        aw_buttons_frame = tkinter.Frame(awailable_frame,
                                        bg='yellow',
                                        bd=FRAME_BORDER)
        aw_buttons_frame.pack(side='top', fill='x', expand=False)

        BUTTONS = (
            ('ADD',    'add'),
            ('DEL',    'del'),
            ('RELOAD', 'reload')
            )

        button_opt = {'side': 'left',
                      'fill': 'x',
                      'expand': True}
        for title, name in BUTTONS:
            self.buttons[name] = tkinter.ttk.Button(aw_buttons_frame,
                                                    text=title)
            self.buttons[name].pack(**button_opt)


class ListCompareModel:
    view = None

    lists = {}

    def __init__(self, view_):
        self.view = view_

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

    def reloadLists(self):
        print('RELOAD')
        # LISTS_DIR = 'lists'
        # curdir = os.path.abspath(os.path.curdir)
        # LISTS_PATH = os.path.normpath(os.path.join(curdir, LISTS_DIR))
        # print(LISTS_PATH)
        # awailable = self.lists['awailable']
        # awailable[:] = []
        # for list_file in os.listdir(LISTS_PATH):
        #     list_file_fullpath = os.path.join(LISTS_PATH, list_file)
        #     lst = list_check(list_file_fullpath)
        #     if lst.type != listtype.UNKNOWN:
        #         lst.path = list_file_fullpath
        #         print lst.type, lst.name
        #         awailable.append(lst)
        #         self.sortAwailable()
        #         self.displayAwailable()

    def sortAwailable(self):
        lst = self.lists['awailable']
        lst.sort(key=lambda item: (item.type, item.name))

    def displayAwailable(self):
        listbox = self.view.listboxes['awailable']
        textlabel = self.view.textlabels['awailable_stat']
        awailable = self.lists['awailable']

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

class ListCompareController:
    model = None
    view = None

    def __init__(self, view=None, model=None):
        if view == None:
            self.view = ListCompareView()
        else:
            self.view = view
        if model == None:
            self.model = ListCompareModel(self.view)
        else:
            self.model = model

        self.bind_handlers()

        if view == None:
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
        self.model.upSelected()

    def down_handler(self, event):
        print('down handler')
        self.model.downSelected()

    def list_handler(self, event):
        print('list handler')
        self.model.listCompare()

    def add_handler(self, event):
        print('add handler')
        self.model.addList()

    def del_handler(self, event):
        print('del handler')
        self.model.delList()

    def reload_handler(self, event):
        print('reload handler')
        self.model.reloadLists()

    def result_sort_handler_name(self, event):
        print('result sort handler name')
        self.model.resultSortChange('name')

    def result_sort_handler_year(self, event):
        print('result sort handler year')
        self.model.resultSortChange('year')

    def close_handler(self):
        print('close')
        self.view.close()


class ListCompareApp:
    controller = None

    def __init__(self):
        self.controller = ListCompareController()
