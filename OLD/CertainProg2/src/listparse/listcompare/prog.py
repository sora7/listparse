'''
Created on 24.05.2014

@author: alex
'''

from view import ListCompareView
from model import  ListCompareModel
from controller import ListCompareController

class ListCompareProg(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        view = ListCompareView()
        model = ListCompareModel(view)
        ListCompareController(view, model, standalone=True)
        