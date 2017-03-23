from listparse.ost_grabber import OSTGrabber


class TenshiOstModel(object):
    view = None

    __grabber = None

    def __init__(self, view_):
        self.view = view_

        self.__grabber = OSTGrabber()

    def reload(self):
        print('reload')
        self.__grabber.fetch_titles()
        self.view.display_available(self.__grabber.titles)

    def add_titles(self):
        pass

    def del_titles(self):
        pass

    def load(self):
        pass

