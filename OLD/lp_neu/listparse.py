# -*- coding: utf-8 -*-

from pprint import pprint
import os

from lp.encap import *
from lp.containers import *
from lp.parsers.anidb import parse_company, parse_person

# txt = proc_file('f:\\PROG\\Python\\class.txt')
# print(txt)


def test():
    mj = 'AniDB.net  Person - Maeda Jun.htm'
    hk = 'AniDB.net  Person - Hanazawa Kana.htm'

    filename = hk
    curr = os.path.abspath(os.curdir)
    filepath = os.path.join(curr, 'lists', filename)

    with open(filepath, encoding='utf-8') as f:
        txt = f.read()

    print('???')
    print('???')
    print('麻枝准')
    # # print(txt[11100:11230])
    # # print(txt[0:len(txt)])
    # print(txt.encode('utf-8'))

    parse_person(txt)


if __name__ == '__main__':
    test()
    pass
