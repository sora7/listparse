from listparse.ui.tenshiost.controller import TenshiOstController


class TenshiOstApp:
    controller = None

    def __init__(self):
        self.controller = TenshiOstController()
