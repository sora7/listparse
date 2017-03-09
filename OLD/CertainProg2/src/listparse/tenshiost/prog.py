'''
Created on 26.05.2014

@author: alex
'''

from view import TenshiOSTView
from model import TenshiOSTModel
from controller import TenshiOSTController

class TenshiOSTApp(object):
    
    def __init__(self):
        view = TenshiOSTView()
        model = TenshiOSTModel(view)
        TenshiOSTController(view, model, standalone=True)