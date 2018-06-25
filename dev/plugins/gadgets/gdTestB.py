"""
Gadget Plugin for Testing
"""
from com.Globals import *

import random

import dev.Gadget as Gadget
import dev.Variable as Variable

#######

EZPID = 'gdTestB'
PTYPE = PT_SENSOR
PNAME = 'Test Gadget B'
PINFO = 'Fusce dolor leo, ornare vitae dolor nec, varius aliquam tellus.'

class PluginGadget(Gadget.PluginGadgetBase):

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'B', 
            'ENABLE':False,
            'TIMER':5,
            # instance specific params
            'abc':12345, 
            'xyz':67890
            }

# -----

    def init(self):
        super().init()
        Variable.set_meta2(self.param['NAME'], 'Voltage', 'Volt', '{:.1f}')

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self, prepare:bool):
        log(5, 'ggTestB Timer')
        Variable.set2(self.param['NAME'], 'Voltage', random.random()*23.0)
