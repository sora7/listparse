# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="alex"
__date__ ="$02.08.2014 13:57:44$"

class TenshiOSTController(object):
    model = None
    view = None
    
    def __init__(self, view, model, standalone=True):
        self.view = view
        self.model = model
        
        self.bind_handlers()

        if standalone:
            # standalone
            self.view.root.protocol('WM_DELETE_WINDOW', self.close_handler)
            self.view.root.mainloop()        

    def close_handler(self):
        self.view.close()

    def bind_handlers(self):
        pass
    