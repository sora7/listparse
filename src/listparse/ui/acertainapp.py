import tkinter
import tkinter.ttk

import listparse.ui.listcompare as lc
import listparse.ui.tenshiost as to


class ACertainView:
    __root = None

    tabs = {}
    listCompare = None
    tenshiOst = None

    def __init__(self):
        self.create_ui()
        self.listCompare = lc.ListCompareView(root=self.__root,
                                              main_frame=
                                              self.tabs['list_compare'])
        self.tenshiOst = to.TenshiOstView(root=self.__root,
                                          main_frame=self.tabs['tenshi_ost'])

    @property
    def root(self):
        return self.__root

    def create_ui(self):
        self.__root = tkinter.Tk()
        root = self.__root
        root.title('A Certain Program')
        w = 600
        h = 500
        self.__root.geometry('%sx%s+0+0' % (w, h))

        notebook = tkinter.ttk.Notebook(self.__root)
        notebook.pack(fill='both', expand=True)

        TABS = (
            ('list_compare', 'List Compare'),
            # ('auto_dir_make', 'AutoDirMake'),
            # ('res_copy', 'ResCopy'),
            # ('wh_scan', 'WH Scan'),
            ('tenshi_ost', 'Tenshi OST'),
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

    listCompare = None
    tenshiOst = None
    ##

    def __init__(self, view):
        self.view = view
        self.listCompare = lc.ListCompareModel(view.listCompare)
        self.tenshiOst = to.TenshiOstModel(view.tenshiOst)


class ACertainController:
    view = None
    model = None

    listCompare = None
    tenshiOst = None

    def __init__(self):
        self.view = ACertainView()
        self.model = ACertainModel(self.view)

        self.listCompare = lc.ListCompareController(self.view.listCompare,
                                                    self.model.listCompare)

        self.listCompare = to.TenshiOstController(self.view.tenshiOst,
                                                  self.model.tenshiOst)

        self.view.root.protocol('WM_DELETE_WINDOW', self.close_handler)
        self.view.root.mainloop()

    def close_handler(self):
        self.view.close()


class ACertainApp:
    controller = None

    def __init__(self):
        self.controller = ACertainController()
