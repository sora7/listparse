# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="alex"
__date__ ="$29.07.2014 17:31:23$"
    
import abc
import Tkinter
import ttk

class BaseView(object):
    __metaclass__ = abc.ABCMeta
    __root = None
    
    __w = None
    __h = None
    __x = None
    __y = None
    __title = None
    
    def __init__(self, root=None, main_frame=None):
        self.__read_param()
        self.__create_ui(root, main_frame)
    
    def __create_ui(self, root, main_frame):
        if root == None:
            # standalone
            self.__root = Tkinter.Tk()
            params = self._param()
            self.__root.title(params['title'])
            geom = (params['w'], params['h'], params['x'], params['y'])
            self.__root.geometry('%sx%s+%s+%s' % geom)
        else:
            # inside
            self.__root = root
        
        self.__mk_main_frame(main_frame)
    
    def __mk_main_frame(self, main_frame):
        if main_frame == None:
            # standalone
            main = Tkinter.Frame(master=self.__root,
                                 bg='black',
                                 bd=self.__BD)
            main.pack(fill='both', expand=True)
        else:
            # inside
            main = main_frame
            
        self._mk_widgets(main)
    
    def __read_param(self):
        params = self._param()
        self.__w = params['w']
        self.__h = params['h']
        self.__x = params['x']
        self.__y = params['y']
        self.__title = params['title']
        self.__BD = params['BD']
    
    abc.abstractmethod
    def _param(self):
        {
         'x' : '0',
         'y' : '0',
         'w' : '0',
         'h' : '0',
         'title' : 'program',
         'BD' : 3
         }
        return
    
    abc.abstractmethod
    def _mk_widgets(self, main_frame):
        return 
    
    @property
    def root(self):
        return self.__root
    
    @property
    def bd(self):
        return self.__BD
    
    def close(self):
        self.__root.destroy()
        self.__root.quit()

def mk_scrollable_area(frame, obj, obj_frame, sbars):
    obj.grid(row=0, column=0, sticky='NSWE')

    if 'y' in sbars:
        yscrollBar = Tkinter.Scrollbar(obj_frame)
        yscrollBar.grid(row=0, column=1, sticky='NS')
        yscrollBar['command'] = obj.yview
        obj['yscrollcommand'] = yscrollBar.set
    if 'x' in sbars:
        xscrollBar = Tkinter.Scrollbar(obj_frame, orient='horizontal')
        xscrollBar.grid(row=1, column=0, sticky='WE')
        xscrollBar['command'] = obj.xview
        obj['xscrollcommand'] = xscrollBar.set
        
    obj_frame.columnconfigure(1, 'minsize')
    obj_frame.columnconfigure(0, weight=1)
    obj_frame.rowconfigure(1, 'minsize')
    obj_frame.rowconfigure(0, weight=1)

def mk_listbox(frame, side='top', sbars='y'):
    BORDER = 0
    COLOR = 'grey'
    
    listbox_frame = Tkinter.Frame(frame, bg=COLOR, bd=BORDER)
    listbox_frame.pack(side=side, fill='both', expand=True)
    
    listbox = Tkinter.Listbox(listbox_frame, selectmode=Tkinter.EXTENDED)
    mk_scrollable_area(frame, listbox, listbox_frame, sbars)
    return listbox

def mk_treeview(frame, side='top', sbars='y'):
    BORDER = 5
    COLOR = 'grey'
    
    treeview_frame = Tkinter.Frame(frame, bg=COLOR, bd=BORDER)
    treeview_frame.pack(side=side, fill='both', expand=True)
    
    treeview = ttk.Treeview(treeview_frame)
    mk_scrollable_area(frame, treeview, treeview_frame, sbars)
    
    return treeview

