#!/usr/bin/env python2

import os
import xml.etree.ElementTree as ET




path = os.path.join(os.path.curdir, 'lists', 'mylist.xml')
print path
tree = ET.parse(path)
root = tree.getroot()
print root.tag
print root.attrib
for child in root:
    print child.tag, child.attrib
    if child.tag == 'animes':
        for title in child:
            print title.tag, title.attrib


def list_mylist5():
    pass
