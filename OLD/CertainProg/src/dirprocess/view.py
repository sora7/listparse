# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="alex"
__date__ ="$09.08.2014 15:26:44$"

import Tkinter
import ttk

from certainprog.ui import mk_treeview

class DirProcessView(object):
    
    frames = {}
    tabs = {}
    
    listboxes = {}
    buttons = {}
    radiobuttons = {}
    checkbuttons = {}
    
    textlabels = {}
    modes = {}
    
    @property
    def root(self):
        return self.__root
    
    def close(self):
        self.__root.destroy()
        self.__root.quit()

    def __init__(self, root=None, main_frame=None):
        self.create_ui(root, main_frame)
    
    def create_ui(self, root, main_frame):
        if root == None:
            # standalone
            self.__root = Tkinter.Tk()
            self.__root.title('Dir Process')
            x, y, w, h = 0, 0, 600, 500
            self.__root.geometry('%sx%s+%s+%s' % (w, h, x, y))
        else:
            # inside
            self.__root = root
            
        self.bd=5
        self.mk_main_frame(main_frame)

    def mk_main_frame(self, main_frame):
        if main_frame == None:
            # standalone
            main = Tkinter.Frame(master=self.__root, bg='black', bd=self.bd)
            main.pack(fill='both', expand=True)
        else:
            # inside
            main = main_frame
            
        self.mk_widgets(main)    
    
    def mk_widgets(self, main_frame):
        command_frame = Tkinter.Frame(master=main_frame, bg='red', bd=self.bd)
        command_frame.pack(fill='both', expand=False)
        
        BUTTONS = (
            ('START', 'start'),
            ('PAUSE', 'pause'),
            ('STOP', 'stop'),
            )
        for title, name in BUTTONS:
            self.buttons[name] = Tkinter.Button(command_frame, text=title)
            self.buttons[name].pack(side='left', fill='both',expand=False)
        #-----------------------------------------------------------------------
        tab_frame = Tkinter.Frame(master=main_frame, bg='green', bd=self.bd)
        tab_frame.pack(fill='both', expand=True)
        
        style = ttk.Style()
        style.configure('WS.TNotebook', tabposition='sw')
        
        notebook = ttk.Notebook(tab_frame, style='WS.TNotebook')
        notebook.pack(fill='both', expand=True)

        TABS = (
            ('selected', 'Selected'),
            ('progress', 'Progress'),
            ('log', 'Log')
            )
        
        for name, title in TABS:
            page = ttk.Frame(self.root)
            
            notebook.add(page, text=title)
            self.tabs[name] = page
        
        #selected page
        selected = self.tabs['selected']
        table_frame = Tkinter.Frame(master=selected, bg='blue', bd=self.bd)
        table_frame.pack(side='left', fill='both', expand=True)
        
        buttons_frame = Tkinter.Frame(master=selected, bg='orange', bd=self.bd)
        buttons_frame.pack(side='left', fill='both', expand=False)
        
        BUTTONS = (
            ('ADD', 'add'),
            ('EDIT', 'edit'),
            ('DEL', 'del'),
            ('UP', 'up'),
            ('DOWN', 'down')
            )
        button_opt = {'side' : 'top', 'fill' : 'x', 'expand' : False}
        for title, name in BUTTONS:
            self.buttons[name] = Tkinter.Button(buttons_frame, text=title)
            self.buttons[name].pack(**button_opt)
            
        table_scroll_frame = Tkinter.Frame(master=table_frame, bg='green', bd=self.bd)
        table_scroll_frame.pack(side='top', fill='both', expand=True)
        
        table = mk_treeview(table_scroll_frame, sbars='xy')
        
        COLUMNS = (
        ('n', '#', 10),
        ('path', 'Path', 200),
        ('status', 'Status', 100),
        )
        
        table['columns'] = list(map(lambda lst: lst[0], COLUMNS))
        for name_, title_, width_ in COLUMNS:
            print name_, title_, width_
            table.column(name_, width=width_)
            table.heading(name_, text=title_)
        
#        table.column("n", width=20)
#        table.column("path", width=100)
#        table.heading("n", text="N")
#        table.heading("path", text="Path")
        
#        table.pack(fill='both', expand=True)
        
        
        #-----------------------------------------------------------------------
        detailed_frame = Tkinter.Frame(master=table_frame, bg='white', bd=self.bd)
        detailed_frame.pack(side='bottom', fill='both', expand=False)
        
        detailed_label = Tkinter.Label(detailed_frame, text='Detailed info:')
        detailed_label.pack(side='left', fill='both', expand=False)