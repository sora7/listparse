'''
Created on 26.05.2014

@author: alex
'''

class TenshiOSTController(object):
    model = None
    view = None
    
    def __init__(self, view, model, standalone=False):
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
        