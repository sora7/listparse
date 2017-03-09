'''
Created on 24.05.2014

@author: alex
'''

import Tkinter
import ttk

from listparse.listcompare.view import ListCompareView
from listparse.listcompare.model import ListCompareModel
from listparse.listcompare.controller import ListCompareController

from listparse.tenshiost.view import TenshiOSTView
from listparse.tenshiost.model import TenshiOSTModel
from listparse.tenshiost.controller import TenshiOSTController

class CertainView:
    __root = None

    tabs = {}
    __listCompare = None
    __tenshiOST = None

    def __init__(self):
        self.__create_ui()
        frame = self.tabs['list_compare']
        self.__listCompare = ListCompareView(root=self.root, main_frame=frame)
        frame = self.tabs['tenshi_ost']
        self.__tenshiOST = TenshiOSTView(root=self.root, main_frame=frame)

    @property
    def listCompare(self):
        return self.__listCompare
    
    @property
    def tenshiOST(self):
        return self.__tenshiOST

    @property
    def root(self):
        return self.__root

    def __create_ui(self):
        self.root = Tkinter.Tk()
        root = self.root
        root.title('A Certain Program')
        w = 650
        h = 500
        self.root.geometry('%sx%s+0+0' % (w, h))
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)

        TABS = (
            ('list_compare', 'List Compare'),
            ('auto_dir_make', 'AutoDirMake'),
            ('res_copy', 'ResCopy'),
            ('wh_scan', 'WH Scan'),
            ('vt_info', 'VideoTime INFO'),
            ('tenshi_ost', 'Tenshi OST'),
            )
        
        for name, title in TABS:
            page = ttk.Frame(self.root)
            
            notebook.add(page, text=title)
            self.tabs[name] = page

    def close(self):
#         print 'close'
        self.root.destroy()
        self.root.quit()
        
'''
Created on 24.05.2014

@author: alex
'''

class CertainModel:
    view = None
    
    listCompare = None
    # #
    # #
    tenshiOST = None

    def __init__(self, view):
        self.view = view
        self.listCompare = ListCompareModel(view.listCompare)
        self.tenshiOST = TenshiOSTModel(view.tenshiOST)
        
'''
Created on 24.05.2014

@author: alex
'''

class CertainController:
    view = None
    model = None

    listCompare = None
    tenshiOST = None

    def __init__(self):
        self.view = CertainView()
        self.model = CertainModel(self.view)

        view = self.view.listCompare
        model = self.model.listCompare
        self.listCompare = ListCompareController(view, model)
        
        view = self.view.tenshiOST
        model = self.model.tenshiOST
        self.tenshiOST = TenshiOSTController(view, model)        

        self.view.root.protocol('WM_DELETE_WINDOW', self.close_handler)
        self.view.root.mainloop()

    def close_handler(self):
        self.view.close()

class CertainProg(object):
    controller = None
    
    def __init__(self):
        self.controller = CertainController()
        