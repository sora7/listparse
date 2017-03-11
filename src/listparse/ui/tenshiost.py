import tkinter
import tkinter.ttk

from listparse.ui.common import mk_listbox

FRAME_BORDER = 0


class TenshiOstView(object):
    __root = None

    listboxes = {}
    buttons = {}

    textlabels = {}

    bd = None

    @property
    def root(self):
        return self.__root

    def close(self):
        self.__root.destroy()
        self.__root.quit()

    def __init__(self, root=None, main_frame=None):
        # self.create_ui(root, main_frame)
        if root is None:
            # standalone
            self.__root = tkinter.Tk()
            self.__root.title('TenshiOST')
            x, y, w, h = 0, 0, 650, 500
            self.__root.geometry('%sx%s+%s+%s' % (w, h, x, y))
        else:
            # inside
            self.__root = root

        self.bd = FRAME_BORDER
        self.mk_main_frame(main_frame)

    def create_ui(self, root, main_frame):
        pass

    def mk_main_frame(self, main_frame):
        if main_frame == None:
            # standalone
            main = tkinter.Frame(master=self.__root, bg='black',bd=self.bd)
            main.pack(fill='both', expand=True)
        else:
            # inside
            main = main_frame

        self.mk_widgets(main)

    def mk_widgets(self, main_frame):
        self.mk_up_frame(main_frame)
        self.mk_search_frame(main_frame)
        self.mk_load_frame(main_frame)

    def mk_up_frame(self, main_frame):
        up_frame = tkinter.Frame(main_frame, bg='green', bd=self.bd)
        up_frame.pack(side='top', fill='x', expand=False)

        savepath_label = tkinter.Label(up_frame, text='Save path')
        savepath_label.pack(side='top', fill='x')

        reload_button = tkinter.ttk.Button(up_frame, text='Reload')
        reload_button.pack(side='bottom', fill='x', expand=True)

        savepath_entry = tkinter.Entry(up_frame, borderwidth=2)
        savepath_entry.pack(side='left', fill='both', expand=True)

        change_savepath_button = tkinter.ttk.Button(up_frame, text='Change')
        change_savepath_button.pack(side='right', fill='x', expand=False)

    def mk_search_frame(self, main_frame):
        search_frame = tkinter.Frame(main_frame, bg='red', bd=self.bd)
        search_frame.pack(side='top', fill='both', expand=True)

        self.mk_awailable_frame(search_frame)
        self.mk_selected_frame(search_frame)

    def mk_awailable_frame(self, search_frame):
        awailable_frame = tkinter.Frame(search_frame, bg='blue', bd=self.bd)
        awailable_frame.pack(side='left', fill='both', expand=True)

        awailable_label = tkinter.Label(awailable_frame, text='Awailable OSTs')
        awailable_label.pack(side='top', fill='x', expand=False)

        awailable_listbox = mk_listbox(awailable_frame, side='left', sbars='y')
        self.listboxes['awailable'] = awailable_listbox

    def mk_selected_frame(self, search_frame):
        selected_frame = tkinter.Frame(search_frame, bg='yellow', bd=self.bd)
        selected_frame.pack(side='right', fill='both', expand=False)

        selected_label = tkinter.Label(selected_frame, text='Selected OSTs')
        selected_label.pack(side='top', fill='x', expand=False)

        selected_listbox = mk_listbox(selected_frame, side='top', sbars='y')
        self.listboxes['selected'] = selected_listbox

        add_button = tkinter.ttk.Button(selected_frame, text='ADD')
        add_button.pack(side='left', fill='x', expand=True)

        del_button = tkinter.ttk.Button(selected_frame, text='DEL')
        del_button.pack(side='right', fill='x', expand=True)

    def mk_load_frame(self, main_frame):
        load_frame = tkinter.Frame(main_frame, bg='blue', bd=self.bd)
        load_frame.pack(side='top', fill='both', expand=False)

        load_button = tkinter.ttk.Button(load_frame, text='LOAD')
        load_button.pack(side='top', fill='x', expand=True)

        log_listbox = mk_listbox(load_frame, side='bottom', sbars='y')


class TenshiOstModel(object):
    view = None

    def __init__(self, view_):
        self.view = view_


class TenshiOstController(object):
    model = None
    view = None

    def __init__(self, view=None, model=None):
        if view is None:
            self.view = TenshiOstView()
        else:
            self.view = view
        if model is None:
            self.model = TenshiOstModel(self.view)
        else:
            self.model = model

        self.bind_handlers()

        if view is None:
            self.view.root.protocol('WM_DELETE_WINDOW', self.close_handler)
            self.view.root.mainloop()

    def close_handler(self):
        self.view.close()

    def bind_handlers(self):
        pass


class TenshiOstApp:
    controller = None

    def __init__(self):
        self.controller = TenshiOstController()
