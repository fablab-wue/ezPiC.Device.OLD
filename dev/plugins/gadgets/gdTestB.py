"""
Gadget Plugin for Testing
"""
from com.Globals import *

import random

import dev.Gadget as Gadget
import dev.Variable as Variable

#######

GDPID = 'TestB'
PNAME = 'Readable Name B'
PINFO = 'Fusce dolor leo, ornare vitae dolor nec, varius aliquam tellus.'

class PluginGadget(Gadget.PluginGadgetBase):

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'name':'B', 
            'enable':True,
            'timer':5000,
            # instance specific params
            'abc':12345, 
            'xyz':67890
            }

# -----

    def init(self):
        super().init()
        Variable.set_meta2(self.param['name'], 'Voltage', 'Volt', '{:.1f}')

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self, prepare:bool):
        log(5, 'ggTestB Timer')
        Variable.set2(self.param['name'], 'Voltage', random.random()*23.0)
