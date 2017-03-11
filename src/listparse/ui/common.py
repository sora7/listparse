import tkinter

FRAME_BORDER = 5

DEFAULTS = {
    'x': 0,
    'y': 0,
    'w': 500,
    'h': 500,
    'title': '% Type Prog Title Here %',
}


class PageView(object):
    __root = None

    bd = None

    def __init__(self, root=None, main_frame=None, param=DEFAULTS):
        if root is None:
            # standalone
            self.__root = tkinter.Tk()
            self.__root.title(param['title'])
            self.__root.geometry('%sx%s+%s+%s' % (param['x'],
                                                  param['y'],
                                                  param['w'],
                                                  param['h']
                                                  ))
        else:
            # inside
            self.__root = root

        self.bd = FRAME_BORDER

        if main_frame is None:
            # standalone
            main_f = tkinter.Frame(master=self.__root, bg='black', bd=self.bd)
            main_f.pack(fill='both', expand=True)
        else:
            # inside
            main_f = main_frame

        self.make_widgets(main_f)

    def make_widgets(self, main_frame):
        pass

    @property
    def root(self):
        return self.__root


def mk_scrollable_area(obj, obj_frame, sbars):
    obj.grid(row=0, column=0, sticky='NSWE')

    if 'y' in sbars:
        yscrollbar = tkinter.ttk.Scrollbar(obj_frame)
        yscrollbar.grid(row=0, column=1, sticky='NS')
        yscrollbar['command'] = obj.yview
        obj['yscrollcommand'] = yscrollbar.set
    if 'x' in sbars:
        xscrollbar = tkinter.ttk.Scrollbar(obj_frame, orient='horizontal')
        xscrollbar.grid(row=1, column=0, sticky='WE')
        xscrollbar['command'] = obj.xview
        obj['xscrollcommand'] = xscrollbar.set

    obj_frame.columnconfigure(1, 'minsize')
    obj_frame.columnconfigure(0, weight=1)
    obj_frame.rowconfigure(1, 'minsize')
    obj_frame.rowconfigure(0, weight=1)


def mk_listbox(frame, side='top', sbars='y', sel_mode=tkinter.EXTENDED):
    BORDER = 0
    COLOR = 'grey'

    listbox_frame = tkinter.Frame(frame, bg=COLOR, bd=BORDER)
    listbox_frame.pack(side=side, fill='both', expand=True)

    listbox = tkinter.Listbox(listbox_frame, selectmode=sel_mode)
    mk_scrollable_area(listbox, listbox_frame, sbars)
    return listbox


def mk_treeview(frame, side='top', sbars='y'):
    BORDER = 5
    COLOR = 'grey'

    treeview_frame = tkinter.Frame(frame, bg=COLOR, bd=BORDER)
    treeview_frame.pack(side=side, fill='both', expand=True)

    treeview = tkinter.ttk.Treeview(treeview_frame)
    mk_scrollable_area(frame, treeview, treeview_frame, sbars)

    return treeview

