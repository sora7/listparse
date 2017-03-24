import tkinter
import tkinter.ttk

from listparse.ui.common import mk_listbox, PageView
from listparse.compare import compare_mode


class ListCompareView(PageView):

    listboxes = {}
    buttons = {}
    radiobuttons = {}

    textlabels = {}
    modes = {}

    def params(self):
        param = {
            'x': 0,
            'y': 0,
            'w': 650,
            'h': 500,
            'title': 'List Compare',
            'bd': 0,
        }
        return param

    def make_widgets(self, main_frame):
        self.modes['result_sort'] = tkinter.StringVar()
        self.modes['result_sort'].set('year')

        # self.modes['list_compare'] = tkinter.StringVar()
        # self.modes['list_compare'].set('intersect')

        self.modes['list_compare'] = tkinter.IntVar()
        self.modes['list_compare'].set(compare_mode.INTERSECT)

        self.textlabels['result_stat'] = tkinter.StringVar()
        self.textlabels['result_stat'].set('count: 0')

        self.textlabels['available_stat'] = tkinter.IntVar()
        self.textlabels['available_stat'].set(0)

        self.textlabels['selected_stat'] = tkinter.IntVar()
        self.textlabels['selected_stat'].set(0)

        self.mk_result_frame(main_frame)
        self.mk_additional_frame(main_frame)

    def mk_result_frame(self, main_frame):
        result_frame = tkinter.Frame(master=main_frame, bg='red',
                                     bd=self.bd)
        result_frame.pack(side='left', fill='both', expand=True)

        tkinter.ttk.Label(result_frame, text='result list').pack(fill='both',
                                                                 side='top')

        self.listboxes['result'] = mk_listbox(result_frame)

        self.mk_statistic_frame(result_frame)

    def mk_statistic_frame(self, result_frame):
        statistic_frame = tkinter.Frame(result_frame, bg='blue',
                                        bd=self.bd)
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
            self.radiobuttons[title] = \
                tkinter.ttk.Radiobutton(statistic_frame,
                                        text=title,
                                        variable=res_sort_mode,
                                        value=value_,
                                        # anchor='w'
                                        )
            self.radiobuttons[title].pack(**radio_opt)

        exp_label = tkinter.ttk.Label(statistic_frame, text='EXPAND')
        exp_label.pack(side='left', fill='both', expand=True)

        stat_label = tkinter.ttk.Label(statistic_frame,
                                       textvariable=
                                       self.textlabels['result_stat']
                                       )
        stat_label.pack(side='left', fill='both')

    def mk_additional_frame(self, main_frame):
        additional_frame = tkinter.Frame(master=main_frame,
                                         bg='blue',
                                         bd=self.bd
                                         )
        additional_frame.pack(side='right', fill='both', expand=False)

        self.mk_selected_frame(additional_frame)
        self.mk_available_frame(additional_frame)

    def mk_selected_frame(self, additional_frame):
        selected_frame = tkinter.Frame(additional_frame,
                                       bg='green',
                                       bd=self.bd)
        selected_frame.pack(side='top', fill='both', expand=True)

        selected_listbox_frame = tkinter.Frame(selected_frame,
                                               bg='blue',
                                               bd=self.bd)
        selected_listbox_frame.pack(side='left', fill='both', expand=True)

        selected_label = tkinter.ttk.Label(selected_listbox_frame,
                                           text='selected lists:')
        selected_label.pack(fill='both')

        self.listboxes['selected'] = mk_listbox(selected_listbox_frame,
                                                side='top')

        sel_stat_label = tkinter.ttk.Label(selected_listbox_frame,
                                           textvariable=
                                           self.textlabels['selected_stat'])
        sel_stat_label.pack(side='left', fill='both')

        sel_stat_text_label = tkinter.ttk.Label(selected_listbox_frame,
                                                text=' lists selected')
        sel_stat_text_label.pack(side='left', fill='both', expand=True)

# #        style = ttk.Style()
# #        style.map('C.TButton',
# #                  foreground=[('pressed','red'),('active','blue')],
# #   background=[('pressed','!disabled','black'),('active','white')]
# #            )
        BUTTONS = (
            ('UP',   'up'),
            ('DOWN', 'down'),
            ('LIST', 'list'),
            )

        # third button will be expand
        exp = 3
        for title, name in BUTTONS:
            exp -= 1
            self.buttons[name] = tkinter.ttk.Button(selected_frame, text=title)
            self.buttons[name].pack(side='top',
                                    fill='both',
                                    expand=not bool(exp))

        mode_label = tkinter.ttk.Label(selected_frame, text='mode:', anchor='n')
        mode_label.pack(side='top', fill='x')

        comp_mode = self.modes['list_compare']

        RADIO = (
            ('intersect', compare_mode.INTERSECT),
            ('differ',    compare_mode.DIFFER),
            ('union',     compare_mode.UNION)
            )

        radio_opt = {'side': 'top', 'fill': 'x'}
        for title, value_ in RADIO:
            tkinter.ttk.Radiobutton(selected_frame,
                                    text=title,
                                    variable=comp_mode,
                                    value=value_
                                    ).pack(**radio_opt)

    def mk_available_frame(self, additional_frame):
        available_frame = tkinter.Frame(additional_frame,
                                        bg='red',
                                        bd=self.bd)
        available_frame.pack(side='top', fill='both', expand=True)

        self.mk_aw_buttons_frame(available_frame)

        aw_label = tkinter.ttk.Label(available_frame, text='available lists:')
        aw_label.pack(side='top', fill='both')

        self.listboxes['available'] = mk_listbox(available_frame)

        aw_stat_label = tkinter.ttk.Label(available_frame,
                                          textvariable=
                                          self.textlabels['available_stat'])
        aw_stat_label.pack(side='left', fill='both')

        aw_stat_text_label = tkinter.ttk.Label(available_frame,
                                               text=' lists available'
                                               )
        aw_stat_text_label.pack(side='left', fill='both', expand=True)

    def mk_aw_buttons_frame(self, available_frame):
        aw_buttons_frame = tkinter.Frame(available_frame,
                                         bg='yellow',
                                         bd=self.bd)
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

    @staticmethod
    def display_listbox(listbox, item_list, countvar):
        listbox.delete(0, tkinter.END)
        for line in item_list:
            listbox.insert(tkinter.END, line)
        listbox.update()
        countvar.set(len(item_list))

