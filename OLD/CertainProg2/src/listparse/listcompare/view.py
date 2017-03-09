'''
Created on 24.05.2014

@author: alex
'''

import Tkinter 

from listparse.ui import BaseView
from listparse.ui import mk_listbox 

class ListCompareView(BaseView):

    frames = {}

    listboxes = {}
    buttons = {}
    radiobuttons = {}
    checkbuttons = {}
    
    textlabels = {}
    modes = {}

    def __init__(self, root=None, main_frame=None):
        BaseView.__init__(self, root, main_frame)

    def _param(self):
        return {
         'x' : '0',
         'y' : '0',
         'w' : '600',
         'h' : '500',
         'title' : 'List Compare',
         'BD' : 3
         }

    def _mk_widgets(self, main_frame):
        self.create_modes()
        self.mk_result_frame(main_frame)
        self.mk_additional_frame(main_frame)

    def create_modes(self):
        self.modes['result_sort'] = Tkinter.StringVar()        
        self.modes['list_compare'] = Tkinter.StringVar()
        self.modes['completed'] = Tkinter.IntVar()
        
        self.textlabels['result_stat'] = Tkinter.StringVar()
        self.textlabels['awailable_stat'] = Tkinter.StringVar()
#defaults@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        self.modes['result_sort'].set('year')
        self.modes['list_compare'].set('intersect')
        self.modes['completed'].set(0)
#defaults@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        self.textlabels['result_stat'].set('count: 0')
        self.textlabels['awailable_stat'].set('0 lists awailable')

    def mk_result_frame(self, main_frame):
        result_frame = Tkinter.Frame(master=main_frame, bg='red', bd=self.BD)
        result_frame.pack(side='left', fill='both', expand=True)

        result_label = Tkinter.Label(result_frame, text='result list')
        result_label.pack(fill='both', side='top')
        
        self.listboxes['result'] = mk_listbox(result_frame, sbars='xy')
        
        self.mk_statistic_frame(result_frame)

    def mk_statistic_frame(self, result_frame):
        statistic_frame = Tkinter.Frame(result_frame, bg='blue', bd=self.BD)
        statistic_frame.pack(side='bottom', fill='both', expand=False)
        
        sort_label = Tkinter.Label(statistic_frame, text='sort:')
        sort_label.pack(side='left', fill='both')
        
        res_sort_mode = self.modes['result_sort']
        
        RADIO = (
            ('name', 'name'),
            ('year', 'year')
            )
        
        radio_opt = {'side' : 'left', 'fill' : 'none'}
        for title, value_ in RADIO:
            self.radiobuttons[title] = Tkinter.Radiobutton(statistic_frame,
                                text=title,
                                variable=res_sort_mode,
                                value=value_,
                                anchor='w')
            self.radiobuttons[title].pack(**radio_opt)

        compl = Tkinter.Checkbutton(statistic_frame,
                                    text='Completed?',
                                    variable=self.modes['completed'],
                                    onvalue=1, offvalue=0)
        compl.pack(side='left', fill='both')
        self.checkbuttons['completed'] = compl

        # exp_label = Tkinter.Label(statistic_frame , text='EXPAND')
        exp_label = Tkinter.Label(statistic_frame)
        exp_label.pack(side='left', fill='both', expand=True)
        
        stat_label = Tkinter.Label(statistic_frame,
                      textvariable=self.textlabels['result_stat'])
        stat_label.pack(side='left', fill='both')

    def mk_additional_frame(self, main_frame):
        additinal_frame = Tkinter.Frame(master=main_frame,
                                                  bg='blue',
                                                  bd=self.BD)
        additinal_frame.pack(side='right', fill='both', expand=False)
        
        self.mk_selected_frame(additinal_frame)
        self.mk_awailable_frame(additinal_frame)

    def mk_selected_frame(self, additinal_frame):
        selected_frame = Tkinter.Frame(additinal_frame, bg='green', bd=self.BD)
        selected_frame.pack(side='top', fill='both', expand=True)

        selectedLabel = Tkinter.Label(selected_frame, text='selected lists')
        selectedLabel.pack(fill='both')
        
        self.listboxes['selected'] = mk_listbox(selected_frame,
                                                     side='left')

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
            self.buttons[name] = Tkinter.Button(selected_frame, text=title)
            self.buttons[name].pack(side='top', fill='both',
                                    expand=not bool(exp))
            
        mode_label = Tkinter.Label(selected_frame, text='mode:', anchor='n')
        mode_label.pack(side='top', fill='x')

        compare_mode = self.modes['list_compare']
                
        RADIO = (
            ('intersect', 'intersect'),
            ('differ', 'differ'),
            ('union', 'union')
            )

        radio_opt = {'side' : 'top', 'fill' : 'x'}
        for title, value_ in RADIO:
            Tkinter.Radiobutton(selected_frame, text=title,
                                variable=compare_mode, value=value_,
                                anchor='w').pack(**radio_opt)

    def mk_awailable_frame(self, additinal_frame):
        awailable_frame = Tkinter.Frame(additinal_frame, bg='red', bd=self.BD)
        awailable_frame.pack(side='top', fill='both', expand=True)

        self.mk_aw_buttons_frame(awailable_frame)

        aw_label = Tkinter.Label(awailable_frame, text='awailable lists')
        aw_label.pack(side='top', fill='both')
        
        stat_label = Tkinter.Label(awailable_frame,
                            textvariable=self.textlabels['awailable_stat'])
        stat_label.pack(side='bottom', fill='both')

        self.listboxes['awailable'] = mk_listbox(awailable_frame)

    def mk_aw_buttons_frame(self, awailable_frame):
        aw_buttons_frame = Tkinter.Frame(awailable_frame,
                                        bg='yellow',
                                        bd=self.BD)
        aw_buttons_frame.pack(side='top', fill='x', expand=False)

        BUTTONS = (
            ('ADD', 'add'),
            ('DEL', 'del'),
            ('RELOAD', 'reload')
            )

        button_opt = {'side' : 'left', 'fill' : 'x', 'expand' : True}
        for title, name in BUTTONS:
            self.buttons[name] = Tkinter.Button(aw_buttons_frame, text=title)
            self.buttons[name].pack(**button_opt)
    
    def display_awailable(self, aw_list):
        listbox = self.listboxes['awailable']
        textlabel = self.textlabels['awailable_stat']
        
        listbox.delete(0, Tkinter.END)
        for item in aw_list:
            listbox.insert(Tkinter.END, '%s ' % (item.name))
        listbox.update()
        
        textlabel.set('%d lists awailable' % (len(aw_list)))
        
    def display_selected(self, sel_list):
        listbox = self.listboxes['selected']
        
        listbox.delete(0, Tkinter.END)
        for item in sel_list:
            listbox.insert(Tkinter.END, '%s' % (item.name))
        listbox.update()
        
    def display_result(self, res_list):
        listbox = self.listboxes['result']
        textlabel = self.textlabels['result_stat']
        
        listbox.delete(0, Tkinter.END)
        for item in res_list:
            listbox.insert(Tkinter.END, '%s %s' % (item.year, item.ani_name))
        
        textlabel.set('count: %i' % len(res_list))
        listbox.update()
        