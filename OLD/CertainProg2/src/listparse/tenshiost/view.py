'''
Created on 26.05.2014

@author: alex
'''

import Tkinter

from listparse.ui import BaseView, mk_listbox

class TenshiOSTView(BaseView):
    
    listboxes = {}
    buttons = {} 
    
    textlabels = {}
    
    def __init__(self, root=None, main_frame=None):
        BaseView.__init__(self, root, main_frame)
        
    def _param(self):
        return {
         'x' : '0',
         'y' : '0',
         'w' : '650',
         'h' : '500',
         'title' : 'TenshiOST',
         'BD' : 3
         }
    
    def _mk_widgets(self, main_frame):
        self.mk_up_frame(main_frame)
        self.mk_search_frame(main_frame)
        self.mk_load_frame(main_frame)
    
    def mk_up_frame(self, main_frame):
        up_frame = Tkinter.Frame(main_frame, bg='green', bd=self.BD)
        up_frame.pack(side='top', fill='x', expand=False)
        
        savepath_label = Tkinter.Label(up_frame, text='Save path')
        savepath_label.pack(side='top', fill='x')

        search_button = Tkinter.Button(up_frame, text='Search')
        search_button.pack(side='bottom', fill='x', expand=True)
        
        savepath_entry = Tkinter.Entry(up_frame, borderwidth=2)
        savepath_entry.pack(side='left', fill='x', expand=True)
        
        change_savepath_button = Tkinter.Button(up_frame, text='Change')
        change_savepath_button.pack(side='right', fill='x', expand=False)
    
    def mk_search_frame(self, main_frame):        
        search_frame = Tkinter.Frame(main_frame, bg='red', bd=self.BD)
        search_frame.pack(side='top', fill='both', expand=True)
        
        self.mk_awailable_frame(search_frame)
        self.mk_selected_frame(search_frame)
    
    def mk_awailable_frame(self, search_frame):
        awailable_frame = Tkinter.Frame(search_frame, bg='blue', bd=self.BD)
        awailable_frame.pack(side='left', fill='both', expand=True)
        
        awailable_label = Tkinter.Label(awailable_frame, text='Awailable OSTs')
        awailable_label.pack(side='top', fill='x', expand=False)
        
        awailable_listbox = mk_listbox(awailable_frame, side='left', sbars='y')
        self.listboxes['awailable'] = awailable_listbox 
    
    def mk_selected_frame(self, search_frame):
        selected_frame = Tkinter.Frame(search_frame, bg='yellow', bd=self.BD)
        selected_frame.pack(side='right', fill='both', expand=False)
        
        selected_listbox = mk_listbox(selected_frame, side='bottom', sbars='y')
        self.listboxes['selected'] = selected_listbox        

        selected_label = Tkinter.Label(selected_frame, text='Selected OSTs')
        selected_label.pack(side='bottom', fill='x', expand=False)
        
        add_button = Tkinter.Button(selected_frame, text='ADD')
        add_button.pack(side='left', fill='x', expand=True)
        
        del_button = Tkinter.Button(selected_frame, text='DEL')
        del_button.pack(side='right', fill='x', expand=True)
        
    def mk_load_frame(self, main_frame):
        load_frame = Tkinter.Frame(main_frame, bg='blue', bd=self.BD)
        load_frame.pack(side='top', fill='both', expand=False)
        
        load_button = Tkinter.Button(load_frame, text='LOAD')
        load_button.pack(side='top', fill='x', expand=True)
        
        log_listbox = mk_listbox(load_frame, side='bottom', sbars='y')