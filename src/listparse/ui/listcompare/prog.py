from listparse.ui.listcompare.controller import ListCompareController


class ListCompareApp:
    controller = None

    def __init__(self):
        self.controller = ListCompareController()
