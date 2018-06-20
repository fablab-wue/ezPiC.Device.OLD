"""
Machine Plugin for Testing on PC
"""
import sys
if sys.platform != 'win32':
    raise Exception()

from com.Globals import *

import dev.Machine as Machine

# PyBoard
#p = Pin_RPi('A8', 1)
#c = Pin_RPi
#pp = c('A10', 1)

#ESP32
#p = Pin_RPi(2, 1)

#LoPy
#p = Pin_RPi('P9', 2)

#######
# Globals:

MAPID = 'TestPC'
PNAME = 'Testing on PC'
PINFO = '???'

LIST_PIN_IO = (
"GPIO0 (Lorem)",
"GPIO1 (Ipsum)",
"GPIO2 (Dolor)",
"GPIO3 (Sit)",
"GPIO4 (Amet)",
)

#######

class PluginMachine(Machine.PluginMachineBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # instance specific params
            'abc':123,
            'xyz':456,
            }

# -----

    def init(self):
        super().init()
        Machine.set_feature('PIN_IO', LIST_PIN_IO)
        Machine.set_feature('PIN_I', LIST_PIN_IO)
        Machine.set_feature('PIN_O', LIST_PIN_IO)

        Machine.set_handler_class('PIN_IO', Pin_PC)

# -----

    def exit(self):
        super().exit()

#######

class Pin_PC():
    IN =            1
    OUT =           2
    OPEN_DRAIN =    3
    PULL_UP =       4
    PULL_DOWN =     5

    def __init__(self, id:str, mode=-1):
        id = str(id).strip().split(' ', 1)[0]
        if id.startswith('GPIO'):
            id = id[4:]
        self._id = int(id)
        self._val = 0
        print('PinPC __init__', id)

    
    def init(self, mode=-1, pull=-1, *, value):
        print('PinPC init', mode, pull)

    def mode(self, m):
        print('PinPC mode', m)

    def set(self, v):
        self._val = v
        print('PinPC set', v)

    def get(self):
        print('PinPC get')
        return self._val

    def value(self, v=None):
        if v:
            self.set(v)
        else:
            return self.get()

    def __call__(self, v=None):
        if v:
            self.set(v)
        else:
            return self.get()

    val = property(get, set)

