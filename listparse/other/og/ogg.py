#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from Tkinter import *
import re
from urllib2 import urlopen
from urllib2 import Request

from og2 import OG

titles = []
loadtitles = []

def search():
    URL = 'http://tenshi.ru/anime-ost/'
    PARENT_DIR = 'tenshi.ru'

    listbox.delete(0,END)
    headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:16.0) Gecko/20120815 Firefox/16.0'}
    req = Request(URL, None, headers)
    url_lines = urlopen(req)

    for line in url_lines:
        match = re.search(r'.*alt="\[DIR\]"> <a href="(.*)"', line)
        if match:
            item = match.group(1)
            if (not re.search(PARENT_DIR,item)) and item != '/' and item != './_unsorted':
                titles.append(item)
                listbox.insert(END,item)

def add_titles():
    item = listbox.get(ANCHOR)
    if len(item) > 0:
        loadlistbox.insert(END,item)

def del_titles():
    loadlistbox.delete(ANCHOR)

def load():
    og = OG()
    og.setOSTdir(save_path.get())
    print save_path.get()
    print "start loading"
    
    lst = loadlistbox.get(0,END)
    for item in lst:
        og.add(item)
        print item

    print len(lst), "titles to download"
    og.grab()
    print "LOAD COMPLETE"

def window_deleted():
    print u'Окно закрыто'
    tk.destroy()
    tk.quit()
    
tk = Tk()
tk.title("OST GRABBER")
tk.geometry('400x500')

## next line for debug only
## comment for not-idle run
##tk.protocol('WM_DELETE_WINDOW', window_deleted)

save_path = StringVar()
save_path.set('/media/Локальный диск/WORKS/OST/')

main = Frame(tk, bg = 'black', bd = 5)
main.pack(fill=BOTH)

label = Label(main,text = "Save path")
label.pack(fill = BOTH)

entry = Entry(main,borderwidth = 2, textvariable = save_path)
entry.pack(fill = BOTH)

sbutton = Button(main,text = "Search",command = search)
sbutton.pack(fill = BOTH)

main2 = Frame(main, bg = 'blue', bd = 5)
main2.pack(fill = BOTH)
##
listframe = Frame(main2, bg = 'green', bd = 5)
listframe.pack(side = 'left', fill = 'both', expand = True)

listbox = Listbox(listframe, height = 15, selectmode = EXTENDED)
listbox.pack(side = 'left', fill = 'both', expand = True)

sbar = Scrollbar(listframe)
sbar.pack(side = 'right', fill = 'y', expand = False)
sbar["command"] = listbox.yview
listbox['yscrollcommand'] = sbar.set

main3 = Frame(main2, bg = 'yellow', bd = 5)
main3.pack(side = 'right', fill = 'x', expand = False)

buttonframe = Frame(main3, bg = 'green', bd = 5)
buttonframe.pack(side = 'top', fill = 'x', expand = False)

addbutton = Button(buttonframe,text = "ADD",command = add_titles)
addbutton.pack(side = 'left', fill = 'both', expand = True)
delbutton = Button(buttonframe,text = "DEL",command = del_titles)
delbutton.pack(side = 'right', fill = 'both', expand = True)

##
loadframe = Frame(main3, bg = 'red', bd = 5)
loadframe.pack(side = 'right', fill = 'x', expand = False)

loadlistbox = Listbox(loadframe, height = 15, selectmode = EXTENDED)
loadlistbox.pack(side = 'left', fill = 'x', expand = True)

sbar2 = Scrollbar(loadframe)
sbar2.pack(side = 'right', fill = 'y', expand = False)
sbar2["command"] = loadlistbox.yview
loadlistbox['yscrollcommand'] = sbar2.set
##
lbutton = Button(main,text = "LOAD",command = load)
lbutton.pack(fill = BOTH)

opframe = Frame(main, bg = 'red', bd = 5)
opframe.pack(fill=BOTH)

op = Text(opframe,width=10,font = 'Arial 10')
op.pack(side = 'left', fill = 'x', expand = True)

sbar2 = Scrollbar(opframe)
sbar2.pack(side = 'right', fill = 'y', expand = False)
sbar2["command"] = op.yview
op['yscrollcommand'] = sbar2.set

tk.mainloop()
