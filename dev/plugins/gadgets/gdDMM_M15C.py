"""
Gadget Plugin for DMM ASCII 15 Byte
Based on ???
"""
from com.Globals import *

import dev.Gadget as Gadget
from . import gdDMM_M14C as M14C

#######
# Globals:

EZPID = 'gdDMM_M15C'
PTYPE = PT_SENSOR
PNAME = 'DMM - ASCII 15 Byte Cont.'

#######

class PluginGadget(M14C.PluginGadget):
    """ TODO """

    def __init__(self, module):
        super().__init__(module, 15)   # 15 byte data packet

# =====

    def is_valid(self):
        if self.data[13] != 0x0D:   # '\r'
            return False
        if self.data[14] != 0x0A:   # '\n'
            return False
        for i in range(13):
            if (self.data[i] & 0x80) != 0x00:
                return False
        return True

#######
