# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="alex"
__date__ ="$09.08.2014 15:26:52$"

class DirProcessModel(object):
    view = None

    reload_lock = None
    compare_lock = None

    lists = {}

    def __init__(self, view):
        self.view = view
        
        self.lists['result'] = []
        self.lists['selected'] = []
        self.lists['awailable'] = []
        