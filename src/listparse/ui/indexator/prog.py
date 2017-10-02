from listparse.ui.indexator.controller import IndexatorController


class IndexatorApp:
    controller = None

    def __init__(self):
        self.controller = IndexatorController()
