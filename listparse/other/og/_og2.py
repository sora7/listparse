# -*- coding: utf-8 -*-
from urllib2 import urlopen
from urllib2 import Request
import re
import os
##CONST
URL='http://tenshi.ru/anime-ost/'
PARENT_DIR = '/anime-ost/'

OST_DIR='/home/alex/Загрузки/OST/'
TITLENAME='Yokohama_Kaidashi_Kikou/'
##TITLENAME='Kino_no_Tabi/'

SAVE_DIR=''.join([OST_DIR,TITLENAME])

dllist1=[]
dllist2=[]
dllist3=[]
os.mkdir(SAVE_DIR)
url = ''.join([URL,TITLENAME])

def find(url):
    headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:16.0) Gecko/20120815 Firefox/16.0'}
    req = Request(url, None, headers)
    u = urlopen(req)
    for line in u:
        match = re.search(r'.*alt="\[DIR\]"> <a href="(.*)"',line)
        if match:
            item = match.group(1)
            if not re.search(PARENT_DIR,item):
                dirpath=re.search(''.join([''.join([URL,TITLENAME]),'(.*)']),''.join([url,item])).group(1)
                #print dirpath
                os.mkdir(''.join([SAVE_DIR,dirpath]))
                #print ''.join([url,item])
                find(''.join([url,item]))
                
        match = re.search(r'.*alt="\[SND\]"> <a href="(.*)"',line)
        if match:
            item = match.group(1)
            if not re.search(PARENT_DIR,item):
                dlitem1={}
                dllk1=''.join([url,item])
                dlpath1=re.search(''.join([''.join([URL,TITLENAME]),'(.*)']),dllk1).group(1)
                dlpath1=''.join([SAVE_DIR,dlpath1])
                dlitem1['link']=dllk1
                dlitem1['file']=dlpath1
                #print dllk1
                dllist1.append(dlitem1)
                pass
        match = re.search(r'.*alt="\[IMG\]"> <a href="(.*)"',line)
        if match:
            item = match.group(1)
            if not re.search(PARENT_DIR,item):
                dlitem2={}
                dllk2=''.join([url,item])
                dlpath2=re.search(''.join([''.join([URL,TITLENAME]),'(.*)']),dllk2).group(1)
                dlpath2=''.join([SAVE_DIR,dlpath2])
                dlitem2['link']=dllk2
                dlitem2['file']=dlpath2
                dllist2.append(dlitem2)
                pass
        match = re.search(r'.*alt="\[VID\]"> <a href="(.*)"',line)
        if match:
            item = match.group(1)
            if not re.search(PARENT_DIR,item):
                dlitem3={}
                dllk3=''.join([url,item])
                dlpath3=re.search(''.join([''.join([URL,TITLENAME]),'(.*)']),dllk3).group(1)
                dlpath3=''.join([SAVE_DIR,dlpath3])
                dlitem3['link']=dllk3
                dlitem3['file']=dlpath3
                dllist3.append(dlitem3)
                pass
        #print line

def download_file(url,path):
    mp3file = urlopen(url)
    output = open(path,'wb')
    output.write(mp3file.read())
    output.close()
             
find(url)

lst=[]
for i in dllist1:
    lst.append(i)
for i in dllist2:
    lst.append(i)
for i in dllist3:
    lst.append(i)

count=0
for d in lst:
    count = count + 1
    print 'downloadind file',count,'of',len(lst)
    print d['link']
    f=d['file']
    f=f.replace('%20',' ')
    d['file']=f
    print d['file']
    download_file(d['link'],d['file'])



##count=0
##for d in dllist1:
##    count = count+ 1
##    print 'downloadind file',count,'of',len(dllist1)
##    print d['link']
##    d=d.replace('%20',' ')
##    print d['file']
##    download_file(d['link'],d['file'])
##
##count=0
##for d in dllist2:
##    count = count+ 1
##    print 'downloadind file',count,'of',len(dllist2)
##    print d['link']
##    print d['file']
##    download_file(d['link'],d['file'])
##
##count=0
##for d in dllist3:
##    count = count+ 1
##    print 'downloadind file',count,'of',len(dllist3)
##    print d['link']
##    print d['file']
##    download_file(d['link'],d['file'])

