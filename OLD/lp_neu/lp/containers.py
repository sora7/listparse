class Title(object):
    __title_id = None
    __title_name = None
    __title_link = None
    __char_id = None
    __char_name = None
    __char_link = None
    __type = None
    __eps = None
    __s_eps = None
    __rating = None
    __year = None
    __year_end = None
    __date_start = None
    __date_end = None
    __complete = None

    def __init(self):
        self.__title_id = None
        self.__title_name = None
        self.__title_link = None
        self.__char_id = None
        self.__char_name = None
        self.__char_link = None
        self.__type = None
        self.__eps = None
        self.__s_eps = None
        self.__rating = None
        self.__year = None
        self.__year_start = None
        self.__year_end = None
        self.__date_start = None
        self.__date_end = None
        self.__complete = None

    @property
    def title_id(self):
        return self.__title_id

    @title_id.setter
    def title_id(self, new_title_id):
        self.__title_id = new_title_id

    @property
    def title_name(self):
        return self.__title_name

    @title_name.setter
    def title_name(self, new_title_name):
        self.__title_name = new_title_name

    @property
    def title_link(self):
        return self.__title_link

    @title_link.setter
    def title_link(self, new_title_link):
        self.__title_link = new_title_link

    @property
    def char_id(self):
        return self.__char_id

    @char_id.setter
    def char_id(self, new_char_id):
        self.__char_id = new_char_id

    @property
    def char_name(self):
        return self.__char_name

    @char_name.setter
    def char_name(self, new_char_name):
        self.__char_name = new_char_name

    @property
    def char_link(self):
        return self.__char_link

    @char_link.setter
    def char_link(self, new_char_link):
        self.__char_link = new_char_link

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, new_type):
        self.__type = new_type

    @property
    def eps(self):
        return self.__eps

    @eps.setter
    def eps(self, new_eps):
        self.__eps = new_eps

    @property
    def s_eps(self):
        return self.__s_eps

    @s_eps.setter
    def s_eps(self, new_s_eps):
        self.__s_eps = new_s_eps

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, new_rating):
        self.__rating = new_rating

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, new_year):
        self.__year = new_year

    @property
    def year_end(self):
        return self.__year_end

    @year_end.setter
    def year_end(self, new_year_end):
        self.__year_end = new_year_end

    @property
    def date_start(self):
        return self.__date_start

    @date_start.setter
    def date_start(self, new_date_start):
        self.__date_start = new_date_start

    @property
    def date_end(self):
        return self.__date_end

    @date_end.setter
    def date_end(self, new_date_end):
        self.__date_end = new_date_end

    @property
    def complete(self):
        return self.__complete

    @complete.setter
    def complete(self, new_complete):
        self.__complete = new_complete


def print_title():
    pass
