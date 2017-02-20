import tkinter
import tkinter.ttk

import listparse.ui.listcompare as lc

class ACertainView:
    root = None

    tabs = {}
    listCompare = None

    def __init__(self):
        self.create_ui()
        self.listCompare = lc.ListCompareView(root=self.root,
                                           main_frame=self.tabs['list_compare'])

    def create_ui(self):
        self.root = tkinter.Tk()
        root = self.root
        root.title('A Certain Program')
        w = 600
        h = 500
        self.root.geometry('%sx%s+0+0' % (w, h))

        notebook = tkinter.ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)

        TABS = (
            ('list_compare', 'List Compare'),
            ('auto_dir_make', 'AutoDirMake'),
            ('res_copy', 'ResCopy'),
            ('wh_scan', 'WH Scan'),
            ('tenshi_ost', 'Tenshi OST'),
            )

        for name, title in TABS:
            page = tkinter.ttk.Frame(self.root)

            notebook.add(page, text=title)
            self.tabs[name] = page

    def close(self):
        print('close')
        self.root.destroy()
        self.root.quit()


class ACertainModel:
    view = None

    listCompare = None
    ##
    ##

    def __init__(self, view):
        self.view = view
        self.listCompare = lc.ListCompareModel(view.listCompare)


class ACertainController:
    view = None
    model = None

    listCompare = None

    def __init__(self):
        self.view = ACertainView()
        self.model = ACertainModel(self.view)

        view = self.view.listCompare
        model = self.model.listCompare
        self.listCompare = lc.ListCompareController(view, model)

        self.view.root.protocol('WM_DELETE_WINDOW', self.close_handler)
        self.view.root.mainloop()

    def close_handler(self):
        self.view.close()


class ACertainApp:
    controller = None

    def __init__(self):
        self.controller = ACertainController()
