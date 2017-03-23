from listparse.ui.tenshiost.view import TenshiOstView
from listparse.ui.tenshiost.model import TenshiOstModel


class TenshiOstController(object):
    model = None
    view = None

    def __init__(self, view=None, model=None):
        if view is None:
            self.view = TenshiOstView()
        else:
            self.view = view
        if model is None:
            self.model = TenshiOstModel(self.view)
        else:
            self.model = model

        self.bind_handlers()

        if view is None:
            self.view.root.protocol('WM_DELETE_WINDOW', self.close_handler)
            self.view.root.mainloop()

    def close_handler(self):
        self.view.close()

    def bind_handlers(self):
        self.view.buttons['reload'].bind("<Button-1>",  self.reload_titles)
        self.view.buttons['add'].bind("<Button-1>",     self.add_titles)
        self.view.buttons['del'].bind("<Button-1>",     self.del_titles)
        self.view.buttons['load'].bind("<Button-1>",    self.load)

    def reload_titles(self, event):
        self.model.reload()

    def add_titles(self, event):
        self.model.add_titles()

    def del_titles(self, event):
        self.model.del_titles()

    def load(self, event):
        self.model.load()

