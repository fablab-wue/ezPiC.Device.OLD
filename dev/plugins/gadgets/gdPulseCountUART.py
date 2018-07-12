"""
Gadget Plugin for CO2 Sensor MH-Z14A and MH-Z19
Based on ???
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdPulseCountUART'
PTYPE = PT_SENSOR
PNAME = 'Pulse Counter (UART)'
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
            'RespVar':'Counts',
            'Scale':'',
            'Mode':'',
            }
        self._readLUT = bytearray(256)
        self._counter = 0

# -----

    def init(self):
        super().init()

        if self._ser:
            self._ser.init(115200, 8, None, 1) # baud=115200 databits=8 parity=none stopbits=1
        #Variable.set_meta(self.param['RespVar'], 'ppm', '{:.0f}')
        self.init_LUT()

# -----

    def exit(self):
        super().exit()

# -----

    def idle(self):
        if not self._ser:
            return

        while self._ser.any():
            data = self._ser.read()
            self._counter += self._readLUT[data]

# -----

    def timer(self, prepare:bool):
        self.idle()

        key = self.param['RespVar']
        source = self.param['NAME']
        Variable.set(key, self.value, source)
            
# =====

    @staticmethod
    def get_hamming_weight(x:int):
        count = 0
        while x:
            x &= x - 1
            count += 1
        
        return count

# -----

    def init_LUT(self):
        for i in range(256):
            count = 1
            self._readLUT[i] = count

#######
