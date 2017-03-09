#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="alex"
__date__ ="$24.07.2014 15:41:35$"

from listcompare.view import ListCompareView
from listcompare.model import ListCompareModel
from listcompare.controller import ListCompareController

def run():
    view = ListCompareView()
    model = ListCompareModel(view)
    ListCompareController(view, model)

if __name__ == "__main__":
    run()
