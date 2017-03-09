#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="alex"
__date__ ="$24.07.2014 15:39:16$"

def certain():
    from certainprog.mvc import CertainController
    print "CertainProg"
    CertainController()

def listcompare():
    from listcompare.view import ListCompareView
    from listcompare.model import ListCompareModel
    from listcompare.controller import ListCompareController
    view = ListCompareView()
    model = ListCompareModel(view)
    ListCompareController(view, model, standalone=True)

def dirprocess():
    pass
#    from dirprocess.whscan import test
#    test() 
#    from dirprocess.process import test
#    test()
#    from dirprocess.view import test
#    test()
    from dirprocess.view import DirProcessView
    from dirprocess.model import DirProcessModel
    from dirprocess.controller import DirProcessController
    view = DirProcessView()
    model = DirProcessModel(view)
    DirProcessController(view, model, standalone=True)

if __name__ == "__main__":
    certain()
#    dirprocess()
    pass