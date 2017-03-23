import tkinter
import tkinter.ttk

import listparse.ui.listcompare.view as lc_v
import listparse.ui.listcompare.model as lc_m
import listparse.ui.listcompare.controller as lc_c

import listparse.ui.tenshiost.view as to_v
import listparse.ui.tenshiost.model as to_m
import listparse.ui.tenshiost.controller as to_c


class ACertainView:
    __root = None

    tabs = {}
    list_compare = None
    tenshi_ost = None

    def __init__(self):
        self.create_ui()
        self.list_compare = lc_v.ListCompareView(root=self.__root,
                                                 main_frame=
                                                 self.tabs['list_compare'])
        self.tenshi_ost = to_v.TenshiOstView(root=self.__root,
                                           main_frame=self.tabs['tenshi_ost'])

    @property
    def root(self):
        return self.__root

    def create_ui(self):
        self.__root = tkinter.Tk()
        # root = self.__root
        self.__root.title('A Certain Program')
        w = 600
        h = 500
        self.__root.geometry('%sx%s+0+0' % (w, h))

        notebook = tkinter.ttk.Notebook(self.__root)
        notebook.pack(fill='both', expand=True)

        TABS = (
            ('list_compare',    'List Compare'),
            ('auto_dir_make',   'AutoDirMake'),
            ('res_copy',        'ResCopy'),
            ('wh_scan',         'WH Scan'),
            ('tenshi_ost',      'Tenshi OST'),
            )

        for name, title in TABS:
            page = tkinter.ttk.Frame(self.__root)

            notebook.add(page, text=title)
            self.tabs[name] = page

    def close(self):
        print('close')
        self.__root.destroy()
        self.__root.quit()


class ACertainModel:
    view = None

    list_compare = None
    tenshi_ost = None
    ##

    def __init__(self, view):
        self.view = view
        self.list_compare = lc_m.ListCompareModel(view.list_compare)
        self.tenshi_ost = to_m.TenshiOstModel(view.tenshi_ost)


class ACertainController:
    view = None
    model = None

    list_compare = None
    tenshi_ost = None

    def __init__(self):
        self.view = ACertainView()
        self.model = ACertainModel(self.view)

        self.list_compare = lc_c.ListCompareController(self.view.list_compare,
                                                       self.model.list_compare)

        self.tenshi_ost = to_c.TenshiOstController(self.view.tenshi_ost,
                                                   self.model.tenshi_ost)

        self.view.root.protocol('WM_DELETE_WINDOW', self.close_handler)
        self.view.root.mainloop()

    def close_handler(self):
        self.view.close()


class ACertainApp:
    controller = None

    def __init__(self):
        self.controller = ACertainController()
