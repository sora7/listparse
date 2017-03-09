#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="alex"
__date__ ="$24.07.2014 15:42:46$"

from tenshiost.view import TenshiOSTView
from tenshiost.model import TenshiOSTModel
from tenshiost.controller import TenshiOSTController

def run():
    view = TenshiOSTView()
    model = TenshiOSTModel(view)
    TenshiOSTController(view, model)

if __name__ == "__main__":
    run()
