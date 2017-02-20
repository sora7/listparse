# -*- coding: utf-8 -*-

# ost grab
# version 0.2
# requires python 2.7

from urllib2 import urlopen
from urllib2 import Request
#from threading import Thread
from time import sleep
import re
import os

class OG:
    URL = 'http://tenshi.ru/anime-ost/'
    PARENT_DIR = '/anime-ost/'
    OST_DIR = ''
    
    titlelist = []
    
    TITLENAME = ''
    SAVE_DIR = ''
    
    ##userful lists
    snd_list = []
    img_list = []
    vid_list = []
    
    def __init__(self):
        pass

    def grab(self):
        count=0
        for titlename in self.titlelist:
            count = count + 1
            print 'LOADING TITLE ', count, ' OF ', len(self.titlelist)
            self.TITLENAME = titlename
            
            self.snd_list = []
            self.img_list = []
            self.vid_list = []
            
            self.SAVE_DIR = ''.join([self.OST_DIR, titlename])
            os.mkdir(self.SAVE_DIR)
            url = ''.join([self.URL, titlename])
            self.find(url)
            download_lst = self.lst_join(self.snd_list, self.img_list, self.vid_list)
            self.download(download_lst)

    def find(self,url):
        headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:16.0) Gecko/20120815 Firefox/16.0'}
        req = Request(url, None, headers)
        url_lines = urlopen(req)
        
        for line in url_lines:
            ##dir
            match = re.search(r'.*alt="\[DIR\]"> <a href="(.*)"', line)
            if match:
                item = match.group(1)
                if not re.search(self.PARENT_DIR,item):
                    dirpath = re.search(''.join([''.join([self.URL, self.TITLENAME]),'(.*)']), ''.join([url, item])).group(1)
                    dirpath = self.fix(dirpath)
                    #print dirpath
                    os.mkdir(''.join([self.SAVE_DIR, dirpath]))
                    #print ''.join([url,item])
                    self.find(''.join([url, item]))
            
            ##sound
            match = re.search(r'.*alt="\[SND\]"> <a href="(.*)"', line)
            if match:
                item = match.group(1)
                if not re.search(self.PARENT_DIR, item):
                    dlitem1 = {}
                    dllk1 = ''.join([url,item])
                    dlpath1 = re.search(''.join([''.join([self.URL, self.TITLENAME]), '(.*)']), dllk1).group(1)
                    dlpath1 = ''.join([self.SAVE_DIR,dlpath1])
                    dlitem1['link'] = dllk1
                    dlitem1['file'] = dlpath1
                    #print dllk1
                    self.snd_list.append(dlitem1)
                    pass
            ##images
            match = re.search(r'.*alt="\[IMG\]"> <a href="(.*)"', line)
            if match:
                item = match.group(1)
                if not re.search(self.PARENT_DIR, item):
                    dlitem2 = {}
                    dllk2 = ''.join([url, item])
                    dlpath2 = re.search(''.join([''.join([self.URL, self.TITLENAME]), '(.*)']), dllk2).group(1)
                    dlpath2 = ''.join([self.SAVE_DIR, dlpath2])
                    dlitem2['link'] = dllk2
                    dlitem2['file'] = dlpath2
                    self.img_list.append(dlitem2)
                    pass
            ##videos
            match = re.search(r'.*alt="\[VID\]"> <a href="(.*)"', line)
            if match:
                item = match.group(1)
                if not re.search(self.PARENT_DIR, item):
                    dlitem3 = {}
                    dllk3 = ''.join([url,item])
                    dlpath3 = re.search(''.join([''.join([self.URL, self.TITLENAME]), '(.*)']), dllk3).group(1)
                    dlpath3 = ''.join([self.SAVE_DIR, dlpath3])
                    dlitem3['link'] = dllk3
                    dlitem3['file'] = dlpath3
                    self.vid_list.append(dlitem3)
                    pass
        #print line
        
    def download_file(self,url,path):
        mp3file = urlopen(url)
        output = open(path,'wb')
        output.write(mp3file.read())
        output.close()
####        os.system('wget -P ' + path + ' ' + url)

    def lst_join(self,list1,list2,list3):
        lst=[]
        for i in list1:
            lst.append(i)
        for i in list2:
            lst.append(i)
        for i in list3:
            lst.append(i)
        return lst 

    def download(self,lst):
        count = 0
        for link2load in lst:
            count = count + 1
            print 'downloading file',count,'of',len(lst)
            l = link2load['link']
            link2load['link'] = l.replace('&amp;','&')
            print link2load['link']
            link2load['file'] = self.fix(link2load['file'])
            print link2load['file']
            
##            t1 = Thread(target=self.download_file, args=(link2load['link'],link2load['file']))
##            t1.start()
##            t1.join()
####            lol = link2load['file']
####            lol = lol.replace(' ','\ ')
####            self.download_file(link2load['link'],lol)
            self.download_file(link2load['link'],link2load['file'])
            sleep(1.5)
        
    def fix(self,s):
        a = s
        a = a.replace('&amp;','&')
        a = a.replace('%5b','[')
        a = a.replace('%5d',']')
        a = a.replace('%20',' ')
        return a
    
    def setOSTdir(self, dir_):
        self.OST_DIR = dir_
    
    def add(self, title):
        if (len(title) != 0):
            if (title[-1] != '/'):
                title = title + '/'
            self.titlelist.append(title)
    
##og = OG()
##og.setOSTdir('/media/Локальный диск/WORKS/OST/')
######
##og.add('Ah_My_Goddess/')
##og.add('Akira/')
##og.add('Angel_Beats/')
##og.add('Azumanga_Daioh/')
######
##og.add('Berserk/')
##og.add('Chrono_Crusade/')
##og.add('Elfen_Lied/')
##og.add('Ergo_Proxy/')
##og.add('FLCL/')
##og.add('Fate.Stay_Night/')
######
##og.add('Abenobashi_Mahou_Shoutengai/')
##og.add('Allison_to_Lillia/')
######
#og.add('GiTS/')
##og.add('Gunbuster/')
##og.add('Green_Green/')
##og.add('Hellsing/')
##og.add('Highschool_of_the_Dead/')
#og.add('Higurashi_no_Naku_Koro_ni/')
######
##og.add('Kara_no_Kyoukai.The_Garden_of_Sinners/')
##og.add('Kare_Kano/')
##og.add('Megazone_23/')
##og.add('Memories/')
##og.add('Mezzo_DSA/')
##og.add('N.H.K/')
##og.add('Najica_Blitz_Tactics/')
##og.add('Neoranga/')
#og.add('Neon_Genesis_Evangelion/')
##og.add('Ore_no_Imouto_ga_Konna_ni_Kawaii_Wake_ga_nai/')
##og.add('Rozen_Maiden/')
##og.add('Lain/')
##og.add('Shakugan_no_Shana/')
##og.add('Shinryaku.Ika_Musume/')
##og.add('Slayers/')
##og.add('The_Melancholy_of_Suzumiya_Haruhi/')
##og.add('To_Aru_Kagaku_no_Railgun/')
##og.add('To_Aru_Majutsu_no_Index/')
##og.add('Toradora/')
#og.add('Aria/')
##og.add('Ayakashi.Japanese_Classic_Horror/')
##og.add('Boogiepop_Phantom/')
##og.add('Dennou_Coil/')
##og.add('Eve_no_Jikan/')
##og.add('Gintama/')
##og.add('Jigoku_Shoujo/')
#og.add('Kamichu/')
##og.add('Kino_no_Tabi/')
##og.add('Mononoke/')
##og.add('Mushishi/')
##og.add('Natsume_Yuujinchou/')
##og.add('Niea_7/')
##og.add('Samurai7/')
##og.add('Shigofumi/')
##og.add('Silent_Mebius/')
##og.add('Sketchbook.Full_Colors/')
##og.add('Sora_no_Woto/')
##og.add('Tamayura/')
##og.add('Tsukihime/')
##og.add('Trigun/')
##og.add('Vampire_Princess_Miyu/')
##og.add('World_Destruction/')
##og.add('Yokohama_Kaidashi_Kikou/')

##og.grab()

