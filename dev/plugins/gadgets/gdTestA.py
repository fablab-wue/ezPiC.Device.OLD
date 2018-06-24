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
PNAME = 'Test Gadget A'
PINFO = 'Lorem ipsum dolor sit amet'

class PluginGadget(Gadget.PluginGadgetBase):

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'A',
            'ENABLE':True,
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
        Variable.set_meta2(self.param['NAME'], self.param['name_t'], '°C', '{:.3f}')

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self, prepare:bool):
        log(5, 'ggTestA Timer')
        Variable.set2(self.param['NAME'], self.param['name_t'], random.random())
