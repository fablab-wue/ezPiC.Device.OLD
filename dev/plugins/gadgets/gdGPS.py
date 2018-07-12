"""
Gadget Plugin for Pulse Counter with UART
Based on ???
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdGPSUART'
PTYPE = PT_SENSOR
PNAME = 'GPS (UART)'
PINFO = ''

#######

class PluginGadget(GS):
    """ TODO """

    def __init__(self, module):
        super().__init__(module, 9)   # 9 byte data packet
        self.param = {
            # must be params
            'NAME':PNAME,
            'ENABLE':False,
            'TIMER':1,
            'PORT':'',
            # instance specific params
            'RespVarLat':'GPS.Lat',
            'RespVarLng':'GPS.Lng',
            }

# -----

    def init(self):
        super().init()

        if self._ser:
            self._ser.init(9600, 8, None, 1) # baud=9600 databits=8 parity=none stopbits=1
        #Variable.set_meta(self.param['RespVar'], 'ppm', '{:.0f}')

# -----

    def exit(self):
        super().exit()

# -----

    def idle(self):
        if not self._ser:
            return

        while self._ser.any():
            data = self._ser.read()
            #self._counter += self._readLUT[data]

# -----

    def timer(self, prepare:bool):
        self.idle()

        key = self.param['RespVarLat']
        source = self.param['NAME']
        Variable.set(key, self.value, source)
            
# =====


#######
