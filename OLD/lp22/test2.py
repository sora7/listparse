#!/usr/bin/env python2

import os
import xml.etree.ElementTree as ET




path = os.path.join(os.path.curdir, 'lists', '  AniDB.net   Person - Hanazawa Kana   .html')
print path
tree = ET.parse(path)
root = tree.getroot()
print root.tag
print root.attrib
for child in root:
    print child.tag, child.attrib

def list_mylist5():
    pass
