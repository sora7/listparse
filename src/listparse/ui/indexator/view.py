import tkinter
import tkinter.ttk

from listparse.ui.common import mk_treeview, PageView


class IndexatorView(PageView):

    listboxes = {}
    buttons = {}

    treeviews = {}
    textlabels = {}

    def __init__(self, root=None, main_frame=None):
        super().__init__(root, main_frame)

    def params(self):
        param = {
            'x': 0,
            'y': 0,
            'w': 650,
            'h': 500,
            'title': 'Indexator',
            'bd': 5,
        }
        return param

    def make_widgets(self, main_frame):
        self.__make_drive_frame(main_frame)
        self.__make_table_frame(main_frame)

    def __make_drive_frame(self, main_frame):
        drive_frame = tkinter.Frame(main_frame, bg='green', bd=self.bd)
        drive_frame.pack(side='left', fill='both', expand=False)

        self.treeviews['drives'] = mk_treeview(drive_frame)

        self.buttons['run_indexator'] = tkinter.ttk.Button(drive_frame,
                                                           text='Run indexator')
        self.buttons['run_indexator'].pack(side='right', fill='x', expand=False)

    def __make_table_frame(self, main_frame):
        table_frame = tkinter.Frame(main_frame, bg='blue', bd=self.bd)
        table_frame.pack(side='left', fill='both', expand=True)

        notebook = tkinter.ttk.Notebook(table_frame)
        notebook.pack(fill='both', expand=True)

        titles_page = tkinter.ttk.Frame(notebook)
        notebook.add(titles_page, text='Titles')

        self.treeviews['titles'] = mk_treeview(titles_page, sbars='xy')

        self.treeviews['titles']['show'] = 'headings'
        self.treeviews['titles']['columns'] = ('one', 'two', 'three')
        self.treeviews['titles'].heading('one', text='Title')
        self.treeviews['titles'].heading('two', text='Year')
        self.treeviews['titles'].column('two', width=40)
        self.treeviews['titles'].heading('three', text='Eps')
        self.treeviews['titles'].column('three', width=40)

        location_page = tkinter.ttk.Frame(table_frame)
        notebook.add(location_page, text='Location')

        self.treeviews['location'] = mk_treeview(location_page)

        self.treeviews['location']['show'] = 'headings'
        self.treeviews['location']['columns'] = ('one', 'two')
        self.treeviews['location'].column('one', width=100)
        self.treeviews['location'].heading('one', text='First')
        self.treeviews['location'].heading('two', text='Second')

        self.treeviews['location'].insert('', 1, text='', values=('1A', '1B'))

        media_page = tkinter.ttk.Frame(table_frame)
        notebook.add(media_page, text='Media')

        self.treeviews['media'] = mk_treeview(media_page)

        self.treeviews['media']['show'] = 'headings'
        self.treeviews['media']['columns'] = ('one', 'two')
        self.treeviews['media'].column('one', width=100)
        self.treeviews['media'].heading('one', text='First')
        self.treeviews['media'].heading('two', text='Second')

        self.treeviews['media'].insert('', 1, text='', values=('1A', '1B'))

        lst = (
            ('Shakugan no Shana', '2005', '25'),
            ('Neon Genesis Evangelion', '1995', '26'),
        )

        self.display_titles(lst)

        lst = (
            ('Toaru Majutsu no Index', '2008', '25'),
        )

        self.display_titles(lst)

    def display_titles(self, lst):
        for i in self.treeviews['titles'].get_children():
            self.treeviews['titles'].delete(i)
        for title in lst:
            self.treeviews['titles'].insert('', 1, text='', values=title)
