#!/usr/bin/env python2

from mechanize import Browser
from time import sleep

def google_it(query):
    br = Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2;\
                    WOW64) AppleWebKit/537.11 (KHTML, like Gecko)\
                    Chrome/23.0.1271.97 Safari/537.11')]
    url = "https://encrypted.google.com/search?hl=ru&q=" + query
    br.open(url)
    links = [l for l in br.links()]
    links_of_interest = []
    for link in links:
        if ("webcache" in link.url and "nyash" in link.url):
##            print link.url
            links_of_interest.append(link.url)
##            return link.url
##    return None
    return links_of_interest

def find_links():
    PAUSE = 0.5
    first = 2
    last = 152+1
    lst = []
    for i in range(first, last):
        query = "nyash.org.ru%2Fpage%2F" + str(i)
        googlen_links = google_it(query)
        for link in googlen_links:
            lst.append({'title':str(i),'link':link})
        print "%i\t%s"%(i,google_it(query))
        sleep(PAUSE)
    return lst
        
def print_list(lst, html = False):
    new_wnd = 'target="_blank"'
##    new_wnd = ''
    if (html):
        print "<!DOCTYPE html> \
            <html> \
            <body> \
            \
            "
    for link in lst:
        if (not html):
            print "%s\t%s"%(link['title'], link['link'])
        else:
            print '<a href="%s" %s >%s</a><br>'%(link['link'],new_wnd,link['title'])
            
    if (html):
        print " \
            </body> \
            </html> \
            \
            "

if __name__ == '__main__':
    lst = find_links()
    print_list(lst, html = True)
