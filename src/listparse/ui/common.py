import tkinter

FRAME_BORDER = 5


class PageView(object):
    __root = None

    bd = None

    def __init__(self, root=None, main_frame=None):
        param = self.params()
        if root is None:
            # standalone
            self.__root = tkinter.Tk()
            self.__root.title(param['title'])
            self.__root.geometry('%sx%s+%s+%s' % (param['w'],
                                                  param['h'],
                                                  param['x'],
                                                  param['y']
                                                  ))
        else:
            # inside
            self.__root = root

        self.bd = param['bd']

        if main_frame is None:
            # standalone
            main_f = tkinter.Frame(master=self.__root, bg='black', bd=self.bd)
            main_f.pack(fill='both', expand=True)
        else:
            # inside
            main_f = main_frame

        self.make_widgets(main_f)

    @property
    def root(self):
        return self.__root

    def close(self):
        self.__root.destroy()
        self.__root.quit()

    # Override
    def make_widgets(self, main_frame):
        pass

    # Override
    def params(self):
        param = {
            'x': 0,
            'y': 0,
            'w': 500,
            'h': 500,
            'title': '% Type Prog Title Here %',
        }
        return param


def mk_scrollable_area(obj, obj_frame, sbars):
    obj.grid(row=0, column=0, sticky='NSWE')

    if 'y' in sbars:
        y_scrollbar = tkinter.ttk.Scrollbar(obj_frame)
        y_scrollbar.grid(row=0, column=1, sticky='NS')
        y_scrollbar['command'] = obj.yview
        obj['yscrollcommand'] = y_scrollbar.set
    if 'x' in sbars:
        x_scrollbar = tkinter.ttk.Scrollbar(obj_frame, orient='horizontal')
        x_scrollbar.grid(row=1, column=0, sticky='WE')
        x_scrollbar['command'] = obj.xview
        obj['xscrollcommand'] = x_scrollbar.set

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
    BORDER = 0
    COLOR = 'grey'

    treeview_frame = tkinter.Frame(frame, bg=COLOR, bd=BORDER)
    treeview_frame.pack(side=side, fill='both', expand=True)

    treeview = tkinter.ttk.Treeview(treeview_frame)
    mk_scrollable_area(treeview, treeview_frame, sbars)

    return treeview

