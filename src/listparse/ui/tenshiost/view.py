import tkinter
import tkinter.ttk

from listparse.ui.common import mk_listbox, PageView


class TenshiOstView(PageView):

    listboxes = {}
    buttons = {}

    textlabels = {}
    text = None
    progress = None

    def __init__(self, root=None, main_frame=None):
        super().__init__(root, main_frame)
        self.text = {}

    def params(self):
        param = {
            'x': 0,
            'y': 0,
            'w': 650,
            'h': 500,
            'title': 'TenshiOST',
            'bd': 0,
        }
        return param

    def make_widgets(self, main_frame):
        self.mk_up_frame(main_frame)
        self.mk_search_frame(main_frame)
        self.mk_load_frame(main_frame)

    def mk_up_frame(self, main_frame):
        up_frame = tkinter.Frame(main_frame, bg='green', bd=self.bd)
        up_frame.pack(side='top', fill='x', expand=False)

        savepath_label = tkinter.Label(up_frame, text='Save path')
        savepath_label.pack(side='top', fill='x')

        savepath_entry = tkinter.Entry(up_frame, borderwidth=2)
        savepath_entry.pack(side='left', fill='both', expand=True)

        self.buttons['savepath'] = tkinter.ttk.Button(up_frame, text='Change')
        self.buttons['savepath'].pack(side='right', fill='x', expand=False)

    def mk_search_frame(self, main_frame):
        search_frame = tkinter.Frame(main_frame, bg='red', bd=self.bd)
        search_frame.pack(side='top', fill='both', expand=True)

        self.mk_available_frame(search_frame)
        self.mk_actions_frame(search_frame)
        self.mk_selected_frame(search_frame)

    def mk_available_frame(self, search_frame):
        available_frame = tkinter.Frame(search_frame, bg='blue', bd=self.bd)
        available_frame.pack(side='left', fill='both', expand=True)

        self.listboxes['available'] = mk_listbox(available_frame,
                                                 side='bottom',
                                                 sbars='y')

        available_label = tkinter.Label(available_frame, text='Available OSTs')
        available_label.pack(side='left', fill='both', expand=True)

        self.buttons['reload'] = tkinter.ttk.Button(available_frame,
                                                    text='Reload')
        self.buttons['reload'].pack(side='left', fill='x')

    def mk_actions_frame(self, search_frame):
        actions_frame = tkinter.Frame(search_frame, bg='black', bd=self.bd)
        actions_frame.pack(side='left', fill='both', expand=False)

        label_filler1 = tkinter.Label(actions_frame, text='')
        label_filler1.pack(side='top', fill='both', expand=True)

        button_width = 5
        self.buttons['add'] = tkinter.ttk.Button(actions_frame, text='>',
                                                 width=button_width)
        self.buttons['add'].pack(side='top', fill='none')

        self.buttons['del'] = tkinter.ttk.Button(actions_frame, text='<',
                                                 width=button_width)
        self.buttons['del'].pack(side='top', fill='none')

        label_filler2 = tkinter.Label(actions_frame, text='')
        label_filler2.pack(side='top', fill='both', expand=True)

    def mk_selected_frame(self, search_frame):
        selected_frame = tkinter.Frame(search_frame, bg='yellow', bd=self.bd)
        selected_frame.pack(side='right', fill='both', expand=False)

        selected_label = tkinter.Label(selected_frame, text='Selected OSTs')
        selected_label.pack(side='top', fill='x', expand=False)

        self.listboxes['selected'] = mk_listbox(selected_frame,
                                                side='bottom',
                                                sbars='y')

    def mk_load_frame(self, main_frame):
        load_frame = tkinter.Frame(main_frame, bg='blue', bd=self.bd)
        load_frame.pack(side='top', fill='both', expand=False)

        self.listboxes['log'] = mk_listbox(load_frame, side='bottom', sbars='y')

        label_log = tkinter.Label(load_frame, text='Log:', anchor='w')
        label_log.pack(side='bottom', fill='x')

        self.buttons['load'] = tkinter.ttk.Button(load_frame, text='LOAD')
        self.buttons['load'].pack(side='left', fill='x')

        self.progress = tkinter.ttk.Progressbar(load_frame, mode='determinate')
        self.progress.pack(side='left', fill='both', expand=True)

        self.textlabels['progress'] = tkinter.IntVar()
        label_progress = tkinter.Label(load_frame,
                                       textvariable=self.textlabels['progress'])
        label_progress.pack(side='left', fill='y')

        label_progress_text = tkinter.Label(load_frame, text='%')
        label_progress_text.pack(side='left', fill='y')

    @staticmethod
    def display_listbox(listbox, lst):
        listbox.delete(0, tkinter.END)
        for line in lst:
            listbox.insert(tkinter.END, line)
        listbox.update()

    def log_add(self, text):
        self.listboxes['log'].insert(tkinter.END, text)
