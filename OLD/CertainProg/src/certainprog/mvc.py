# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="alex"
__date__ ="$29.07.2014 17:30:24$"

import Tkinter
import ttk

from listcompare.view import ListCompareView
from listcompare.model import ListCompareModel
from listcompare.controller import ListCompareController

from dirprocess.view import DirProcessView
from dirprocess.model import DirProcessModel
from dirprocess.controller import DirProcessController

from tenshiost.view import TenshiOSTView
from tenshiost.model import TenshiOSTModel
from tenshiost.controller import TenshiOSTController

class CertainView:
    __root = None

    tabs = {}
    listCompare = None
    dirProcess = None
    tenshiOST = None

    def __init__(self):
        self.__create_ui()
        frame = self.tabs['list_compare']
        self.listCompare = ListCompareView(root=self.root, main_frame=frame)
        frame = self.tabs['dir_process']
        self.dirProcess = DirProcessView(root=self.root, main_frame=frame)
        frame = self.tabs['tenshi_ost']
        self.tenshiOST = TenshiOSTView(root=self.root, main_frame=frame)

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
            ('dir_process', 'DirProcess'),
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
        
class CertainModel:
    view = None
    
    listCompare = None
    dirProcess = None
    # #
    # #
    tenshiOST = None

    def __init__(self, view):
        self.view = view
        self.listCompare = ListCompareModel(view.listCompare)
        self.dirProcess = DirProcessModel(view.dirProcess)
        self.tenshiOST = TenshiOSTModel(view.tenshiOST)

class CertainController:
    view = None
    model = None

    listCompare = None
    dirProcess = None
    tenshiOST = None

    def __init__(self):
        self.view = CertainView()
        self.model = CertainModel(self.view)

        view = self.view.listCompare
        model = self.model.listCompare
        self.listCompare = ListCompareController(view, model, standalone=False)

        view = self.view.dirProcess
        model = self.model.dirProcess
        self.dirProcess = DirProcessController(view, model, standalone=False)        
        
        view = self.view.tenshiOST
        model = self.model.tenshiOST
        self.tenshiOST = TenshiOSTController(view, model, standalone=False)

        self.view.root.protocol('WM_DELETE_WINDOW', self.close_handler)
        self.view.root.mainloop()

    def close_handler(self):
        self.view.close()
