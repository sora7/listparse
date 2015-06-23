'''
Created on 18.03.2014

@author: alex
'''

import os
import Tkinter

from listparse import keys
from listparse import list_check, list_person, list_company, list_mylist
from listparse import list_diff, list_inter, print_list

################################################################################
# LISTPARSE GUI
################################################################################

class ListCompare:
    # # THE BRAIN ##
    aw_lists = []
    sel_lists = []
    res_list = []
    
    def __init__(self):
        pass

class ListCompareGui:
    # main window
    root = None
    
    aw_listbox = None
    sel_listbox = None
    res_listbox = None
    
    aw_stat_text = None
    res_stat_text = None
    
    compareMode = None
    
    COMPARE_MODES = {
        'intersect' : '0',
        'differ'    : '1',
        'union'     : '2'
        }

    res_sortMode = None
    
    RES_SORT_MODES = {
        'name' : '0',
        'year' : '1'
        }
    
    def add_title_handler(self):
        pass
    
    def del_title_handler(self):
        pass
    
    def up_title_handler(self):
        pass
    
    def down_title_handler(self):
        pass
    
    def list_titles_handler(self):
        pass
    
    def reload_aw_handler(self):
        pass
    
    def __init__(self):
        self.createWidgets()
        
    def createWidgets(self):
        pass

# class ListCompareApp:
#     #listCompareGui
#     #listCompare
#     pass

class ListCompareApp:
    root = None

    aw_Listbox = None
    sel_Listbox = None
    res_Listbox = None

    aw_stat_Text = None
    res_list_Text = None
    #---------------
    compareMode = None
    res_sortMode = None
    
    settings = {}
    ###################
    aw_lists = []
    sel_lists = []
    res_list = []
    ###################

    COMPARE_MODES = {
        'intersect' : '0',
        'differ'    : '1',
        'union'     : '2'
        }
    
    RES_SORT_MODES = {
        'name' : '0',
        'year' : '1'
        }

    ################
    ### HANDLERS ###
    ################

    def add_t(self):
        items = sorted(map(int, self.aw_Listbox.curselection()), reverse=True)
        for i in items:
            self.sel_lists.append(self.aw_lists.pop(i))

        self.sort_aw()
        self.display_aw()
        self.display_sel()
        # self.display_lists()

    def del_t(self):
        items = sorted(map(int, self.sel_Listbox.curselection()),
                       reverse=True)
        for i in items:
            self.aw_lists.append(self.sel_lists.pop(i))
            
        self.sort_aw()
        self.display_aw()
        self.display_sel()
        # self.display_lists()
    
    def up_t(self):
        indexes = map(int, self.sel_Listbox.curselection())
        print 'old', indexes
        new = [i for i in indexes]
        for i in indexes:
            if i != indexes.index(i):
                (self.sel_lists[i],
                 self.sel_lists[i - 1]) = (self.sel_lists[i - 1],
                                           self.sel_lists[i])
                new[indexes.index(i)] -= 1
        print 'new', new
        # name = tkFileDialog.askopenfilename()
        self.display_sel()
        # self.display_lists()
        
        for i in new:
            self.sel_Listbox.selection_set(i, i)

    def down_t(self):
        indexes = sorted(map(int, self.sel_Listbox.curselection()),
                         reverse=True)
        print 'old', indexes
        new = [i for i in indexes]
        for i in indexes:
            if i != self.sel_Listbox.size() - indexes.index(i) - 1:
                (self.sel_lists[i],
                 self.sel_lists[i + 1]) = (self.sel_lists[i + 1],
                                         self.sel_lists[i])
                new[indexes.index(i)] += 1
        print 'new', new
        
        self.display_sel()
        # self.display_lists()
        for i in new:
            self.sel_Listbox.selection_set(i, i)

    def load_t(self):
        self.checkAwailableLists()
        self.display_lists()

    def list_t(self):
        lists = []
        for item in self.sel_lists:
            if item != None:
                if item[keys.LIST_TYPE] == keys.FTYPE_PERSON:
                    lst = list_person(item['file'])
                if item[keys.LIST_TYPE] == keys.FTYPE_COMPANY:
                    lst = list_company(item['file'])
                if item[keys.LIST_TYPE] == keys.FTYPE_MYLIST:
                    lst = list_mylist(item['file'])
                lists.append(lst)
        res = []
        if (self.compareMode.get() == self.COMPARE_MODES['intersect']):
            res = list_inter(lists)
        elif (self.compareMode.get() == self.COMPARE_MODES['differ']):
            res = list_diff(lists[0:2])
        elif (self.compareMode.get() == self.COMPARE_MODES['union']):
            for lst in lists:
                for item in lst:
                    res.append(item)            
        self.res_list = res
        # print_list(self.res_list)
        self.display_lists()
    
    def __init__(self):        
        self.root = Tkinter.Tk()
        self.root.title('A Certain Title')
        w = 600
        h = 500
        self.root.geometry('%sx%s+0+0' % (w, h))
        
        self.createWidgets()

        # import_modules()
        self.reloadSettings()
        # self.checkAwailableLists()

        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.root.mainloop()

    def close(self):
        print 'close'
        self.root.destroy()
        self.root.quit()
        
    def reloadSettings(self):
        self.settings = {
            'LISTS_PATH' : 'lists'
            }
    
    def checkAwailableLists(self):
        lists_dir = self.settings['LISTS_PATH']
        lists_path = os.path.join(os.path.abspath(os.path.curdir), lists_dir)

        self.aw_lists = []
        self.sel_lists = []
        
        for item in os.listdir(lists_path):
            item_fullpath = os.path.join(lists_path, item)
            data = list_check(item_fullpath)
            print 'DATA:', data
            if data != None:
                data['file'] = item_fullpath
                self.aw_lists.append(data)
                # print '',;
                # self.display_lists()
                self.sort_aw()
                self.display_aw()
                # self.root.update()
        self.sort_aw()
        self.display_aw()
        # self.display_lists()
        # print self.c

    ########################
    ### SORT AND DISPLAY ###
    ########################

    def sort_aw(self):
        # type, name
        # print self.aw_lists[0]
        self.aw_lists.sort(key=lambda item : (item[keys.LIST_TYPE],
                                              item[keys.LIST_NAME]))

    def sort_res(self):
        if self.res_sortMode.get() == self.RES_SORT_MODES['year']:
            self.res_list.sort(key=lambda item : item.year)
            print 'year'
        elif self.res_sortMode.get() == self.RES_SORT_MODES['name']:
            self.res_list.sort(key=lambda item : item.ani_name)
            print 'name'

    def sort_lists(self):
        self.sort_aw()
        self.sort_res()

    def display_aw(self):
        self.aw_Listbox.delete(0, Tkinter.END)
        for aw_list in self.aw_lists:
            self.aw_Listbox.insert(Tkinter.END, '%s' % (aw_list[keys.LIST_NAME]))
        self.aw_Listbox.update()
        self.aw_stat_Text.set('%d lists awailable' % (len(self.aw_lists)))

    def display_sel(self):
        self.sel_Listbox.delete(0, Tkinter.END)
        for sel_list in self.sel_lists:
            self.sel_Listbox.insert(Tkinter.END, '%s' % (sel_list[keys.LIST_NAME]))
        self.sel_Listbox.update()

    def display_res(self):
        self.res_Listbox.delete(0, Tkinter.END)
        uniq = []
        for item in self.res_list:
            if item.ani_name not in uniq:
                uniq.append(item.ani_name)
                self.res_Listbox.insert(Tkinter.END, '%s %s' % (item.year, item.ani_name))
                self.res_list_Text.set('count: %i' % len(self.res_list))
        self.res_list_Text.set('count: %i' % len(self.res_list))

    def display_lists(self):
        # print 'display'
        self.sort_lists()
        self.display_aw()
        self.display_sel()
        self.display_res()

    def backcall(self, event):
        print 'F pressed'

    ##################
    ### GUI CREATE ###
    ##################

    def createWidgets(self):
        # button_opt = {'side' : 'left', 'fill' : 'x', 'expand' : True}
        FRAME_BORDER = 3
        colors = {
            'main'       : 'black',
            'result'     : 'red',
            'st'         : 'blue',
            'add'        : 'blue',
            'sel'        : 'green',
            'aw'         : 'red',
            'aw_buttons' : 'yellow'
            }
        FRAMES = {
            'main' : {
                'opt'  : {
                    'bg' : colors['main'], 'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'fill'   : 'both', 'expand' : True
                    }
                },
            'res' : {
                'opt' : {
                    'bg' : colors['result'], 'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'side'   : 'left', 'fill'   : 'both', 'expand' : True
                    }
                },
            'add' : {
                'opt' : {
                    'bg' : colors['add'], 'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'side'   : 'right', 'fill'   : 'both', 'expand' : False
                    }
                },
            'sel' : {
                'opt' : {
                    'bg' : colors['sel'], 'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'side'   : 'top', 'fill'   : 'both', 'expand' : True
                    }
                },
            'aw' : {
                'opt' : {
                    'bg' : colors['aw'], 'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'side'   : 'right', 'fill'   : 'both', 'expand' : False
                    }
                },
            'st' : {
                'opt' : {
                    'bg' : colors['st'], 'bd' : FRAME_BORDER
                    },
                'pack' : {
                    'side'   : 'bottom', 'fill'   : 'both', 'expand' : False
                    }
                }
            }
        
        main_Frame = Tkinter.Frame(master=self.root, **FRAMES['main']['opt'])
        main_Frame.pack(**FRAMES['main']['pack'])
        ##############################################################
        res_Frame = Tkinter.Frame(master=main_Frame, **FRAMES['res']['opt'])
        res_Frame.pack(**FRAMES['res']['pack'])
        
        Tkinter.Label(res_Frame, text='result list').pack(fill='both',
                                                            side='top')

        self.res_list_Text = Tkinter.StringVar()
        self.res_list_Text.set('count: 0')

        st_Frame = Tkinter.Frame(res_Frame, **FRAMES['st']['opt'])
        st_Frame.pack(**FRAMES['st']['pack'])

        Tkinter.Label(st_Frame, text='sort:').pack(side='left', fill='both')
        self.res_sortMode = Tkinter.StringVar()
        self.res_sortMode.set(self.RES_SORT_MODES['year'])
        
        RADIO = (
            ('name', self.RES_SORT_MODES['name']),
            ('year', self.RES_SORT_MODES['year'])
            )
        
        radio_opt = {'side' : 'left', 'fill' : 'none'}
        for title, value_ in RADIO:
            Tkinter.Radiobutton(st_Frame, text=title,
                                variable=self.res_sortMode, value=value_,
                                anchor='w').pack(**radio_opt)

        Tkinter.Label(st_Frame, text='').pack(side='left',
                                                    fill='both',
                                                    expand=True)
        Tkinter.Label(st_Frame,
                      textvariable=self.res_list_Text).pack(side='left',
                                                              fill='both')
        
        self.res_Listbox = Tkinter.Listbox(res_Frame,
                                                selectmode=Tkinter.EXTENDED)
        self.res_Listbox.pack(side='left', fill='both', expand=True)
        
        res_scrollBar = Tkinter.Scrollbar(res_Frame)
        res_scrollBar.pack(side='right', fill='y', expand=False)
        res_scrollBar['command'] = self.res_Listbox.yview
        self.res_Listbox['yscrollcommand'] = res_scrollBar.set
        ##############################################################
        add_Frame = Tkinter.Frame(master=main_Frame, **FRAMES['add']['opt'])
        add_Frame.pack(**FRAMES['add']['pack'])
        ##############################################################
        sel_Frame = Tkinter.Frame(add_Frame, **FRAMES['sel']['opt'])
        sel_Frame.pack(**FRAMES['sel']['pack'])

        selectedLabel = Tkinter.Label(sel_Frame, text='selected lists')
        selectedLabel.pack(fill='both')

        self.sel_Listbox = Tkinter.Listbox(sel_Frame,
                                           selectmode=Tkinter.EXTENDED)
        self.sel_Listbox.pack(side='left', fill='both', expand=True)
        
        sel_scrollBar = Tkinter.Scrollbar(sel_Frame)
        sel_scrollBar.pack(side='left', fill='y', expand=False)
        sel_scrollBar['command'] = self.sel_Listbox.yview
        self.sel_Listbox['yscrollcommand'] = sel_scrollBar.set

# #        style = ttk.Style()
# #        style.map('C.TButton',
# #                  foreground=[('pressed','red'),('active','blue')],
# #                  background=[('pressed','!disabled','black'),('active','white')]
# #            )
        BUTTONS = (
            ('UP', self.up_t),
            ('DOWN', self.down_t),
            ('LIST', self.list_t),
            )
        
        # third button will be expand
        exp = 3
        for title, command_ in BUTTONS:
            exp -= 1
            Tkinter.Button(sel_Frame, text=title,  # #style = 'C.TButton',
                           command=command_).pack(side='top',
                                                    fill='both',
                                                    expand=not bool(exp))
            
        Tkinter.Label(sel_Frame, text='mode:',
                      anchor='n').pack(side='top', fill='x')

        self.compareMode = Tkinter.StringVar()
        self.compareMode.set(self.COMPARE_MODES['intersect'])
        
        RADIO = (
            ('intersect', self.COMPARE_MODES['intersect']),
            ('differ', self.COMPARE_MODES['differ']),
            ('union', self.COMPARE_MODES['union'])
            )

        radio_opt = {'side' : 'top', 'fill' : 'x'}
        for title, value_ in RADIO:
            Tkinter.Radiobutton(sel_Frame, text=title,
                                variable=self.compareMode, value=value_,
                                anchor='w').pack(**radio_opt)
        ##############################################################
        aw_Frame = Tkinter.Frame(add_Frame, bg=colors['aw'],
                                       bd=FRAME_BORDER)
        aw_Frame.pack(side='top', fill='both', expand=True)
        ##############################################################
        aw_buttonsFrame = Tkinter.Frame(aw_Frame,
                                        bg=colors['aw_buttons'],
                                        bd=FRAME_BORDER)
        aw_buttonsFrame.pack(side='top', fill='x', expand=False)

        BUTTONS = (
            ('ADD', self.add_t),
            ('DEL', self.del_t),
            ('RELOAD', self.load_t)
            )

        button_opt = {'side' : 'left', 'fill' : 'x', 'expand' : True}
        for title, command_ in BUTTONS:
            Tkinter.Button(aw_buttonsFrame, text=title,
                           command=command_).pack(**button_opt)
        
        Tkinter.Label(aw_Frame, text='awailable lists').pack(side='top',
                                                               fill='both')

        self.aw_stat_Text = Tkinter.StringVar()
        self.aw_stat_Text.set('0 lists awailable')

        Tkinter.Label(aw_Frame,
                      textvariable=self.aw_stat_Text).pack(side='bottom',
                                                             fill='both')

        self.aw_Listbox = Tkinter.Listbox(aw_Frame,
                                          selectmode=Tkinter.EXTENDED)
        self.aw_Listbox.pack(side='left', fill='both', expand=True)
        aw_scrollBar = Tkinter.Scrollbar(aw_Frame)
        aw_scrollBar.pack(side='right', fill='y', expand=False)
        aw_scrollBar['command'] = self.aw_Listbox.yview
        self.aw_Listbox['yscrollcommand'] = aw_scrollBar.set

#        self.root.bind('f', self.backcall)

################################################################################

if __name__ == '__main__':
    ListCompareApp()
    pass
