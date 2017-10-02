from listparse.ui.indexator.view import IndexatorView
from listparse.ui.indexator.model import IndexatorModel


class IndexatorController(object):
    model = None
    view = None

    def __init__(self, view=None, model=None):
        if view is None:
            self.view = IndexatorView()
        else:
            self.view = view
        if model is None:
            self.model = IndexatorModel(self.view)
        else:
            self.model = model

        self.bind_handlers()

        if view is None:
            self.view.root.protocol('WM_DELETE_WINDOW', self.close_handler)
            self.view.root.mainloop()

    def close_handler(self):
        self.view.close()

    def bind_handlers(self):
        self.view.buttons['run_indexator'].bind("<Button-1>", self.index_dirs)

    def index_dirs(self, event):
        self.model.run_indexator()


