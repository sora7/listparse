import tkinter
import tkinter.ttk

from listparse.ui.common import mk_listbox, PageView


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

        self.modes['list_compare'] = tkinter.StringVar()
        self.modes['list_compare'].set('intersect')

        self.textlabels['result_stat'] = tkinter.StringVar()
        self.textlabels['result_stat'].set('count: 0')

        self.textlabels['awailable_stat'] = tkinter.StringVar()
        self.textlabels['awailable_stat'].set('0 lists awailable')

        self.mk_result_frame(main_frame)
        self.mk_additional_frame(main_frame)

    def mk_result_frame(self, main_frame):
        result_frame = tkinter.Frame(master=main_frame, bg='red',
                                     bd=self.bd)
        result_frame.pack(side='left', fill='both', expand=True)

        tkinter.ttk.Label(result_frame, text='result list').pack(fill='both',
                                                                 side='top')
        self.mk_statistic_frame(result_frame)

        self.listboxes['result'] = mk_listbox(result_frame)

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
        additinal_frame = tkinter.Frame(master=main_frame,
                                        bg='blue',
                                        bd=self.bd
                                        )
        additinal_frame.pack(side='right', fill='both', expand=False)

        self.mk_selected_frame(additinal_frame)
        self.mk_awailable_frame(additinal_frame)

    def mk_selected_frame(self, additional_frame):
        selected_frame = tkinter.Frame(additional_frame,
                                       bg='green',
                                       bd=self.bd)
        selected_frame.pack(side='top', fill='both', expand=True)

        selectedLabel = tkinter.ttk.Label(selected_frame, text='selected lists')
        selectedLabel.pack(fill='both')

        self.listboxes['selected'] = mk_listbox(selected_frame, side='left')

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
            tkinter.ttk.Radiobutton(selected_frame, text=title,
                                variable=compare_mode, value=value_
                                ).pack(**radio_opt)
            # tkinter.Radiobutton(selected_frame, text=title,
            #                     variable=compare_mode, value=value_,
            #                     anchor='w').pack(**radio_opt)

    def mk_awailable_frame(self, additinal_frame):
        awailable_frame = tkinter.Frame(additinal_frame,
                                        bg='red',
                                        bd=self.bd)
        awailable_frame.pack(side='top', fill='both', expand=True)

        self.mk_aw_buttons_frame(awailable_frame)

        aw_label = tkinter.ttk.Label(awailable_frame, text='awailable lists')
        aw_label.pack(side='top',fill='both')

        stat_label = tkinter.ttk.Label(awailable_frame,
                            textvariable=self.textlabels['awailable_stat'])
        stat_label.pack(side='bottom', fill='both')

        self.listboxes['awailable'] = mk_listbox(awailable_frame)

    def mk_aw_buttons_frame(self, awailable_frame):
        aw_buttons_frame = tkinter.Frame(awailable_frame,
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
