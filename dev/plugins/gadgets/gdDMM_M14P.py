"""
Gadget Plugin for DMM ASCII 14 Byte P
Based on ???
"""
from com.Globals import *

import dev.Gadget as Gadget
from . import gdDMM_M14C as M14C

#######
# Globals:

EZPID = 'gdDMM_M14P'
PTYPE = PT_SENSOR
PNAME = 'DMM - ASCII 14 Byte P'

#######

class PluginGadget(M14C.PluginGadget):
    """ TODO """

    def __init__(self, module, size=14):
        super().__init__(module, size)   # 14 byte data packet
        self.param['TIMER'] = 1

# -----

    def timer(self, prepare:bool):
        super().timer(prepare)

        if self._ser:
            self._ser.write(b'D\n')

#######
