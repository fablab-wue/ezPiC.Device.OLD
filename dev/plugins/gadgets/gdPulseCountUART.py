"""
Gadget Plugin for Pulse Counter with UART
Based on ???
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Timer as Timer

#######
# Globals:

EZPID = 'gdPulseCountUART'
PTYPE = PT_SENSOR
PNAME = '@WORK IO - Pulse Counter (serial)'

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
            #'Mode':'',
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
        self._counter = 0
        self._last_clock = Timer.clock()

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

        counter = self._counter
        clock = Timer.clock()
        clock_diff = clock - self._last_clock
        self._counter = 0
        self._last_clock = clock
        counter *= 1000 / clock_diff
        scale_str = self.param['Scale']
        if scale_str:
            counter *= float(scale_str)

        key = self.param['RespVar']
        source = self.param['NAME']
        Variable.set(key, counter, source)

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
            count = 0
            if get_hamming_weight(i) <= 4:   # majority low
                count = 1
            self._readLUT[i] = count

#######
