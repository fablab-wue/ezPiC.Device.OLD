"""
Gadget Plugin for Testing
"""
from com.Globals import *

import random

import dev.Gadget as Gadget
import dev.Variable as Variable

#######

EZPID = 'gdTestA'
PTYPE = PT_SENSOR
PNAME = 'Test - Gadget A'

class PluginGadget(Gadget.PluginGadgetBase):

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'A',
            'ENABLE':False,
            'TIMER':10,
            # instance specific params
            'name_t':'T',
            'name_h':'H',
            'name_p':'P',
            'abc':123,
            'xyz':456,
            'sel':2,
            'qwe':'Lorem ipsum',
            'asd':[1,2,3,4,5],
            }

# -----

    def init(self):
        super().init()
        Variable.set_meta((self.param['NAME'], self.param['name_t']), '°C', '{:.3f}')

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self, prepare:bool):
        log(5, 'ggTestA Timer')
        Variable.set((self.param['NAME'], self.param['name_t']), random.random())
