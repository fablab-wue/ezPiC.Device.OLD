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

EZPID = 'gdGasSer_CO2_MHZ1x'
PTYPE = PT_SENSOR
PNAME = 'CO2 MH-Z14/19 (UART)'
PINFO = 'Winsen MH-Z14A; MH-Z19'

COMMAND_READ = b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79'

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
            'RespVar':'CO2',
            }

# -----

    def init(self):
        super().init()

        if self._ser:
            self._ser.init(9600, 8, None, 1) # baud=9600 databits=8 parity=none stopbits=1
        Variable.set_meta(self.param['RespVar'], 'ppm', '{:.0f}')

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self, prepare:bool):
        while self.process():
            print(self.value, self.unit, self.form)
            key = self.param['RespVar']
            source = self.param['NAME']
            Variable.set(key, self.value, source)
        if self._ser:
            self._ser.write(COMMAND_READ)

# =====

    def is_valid(self):
        if self.data[0] != 0xFF:   # Starting
            return False
        if self.data[1] != 0x86:   # Command.
            return False
        sum = 0
        for i in range(1, 8):
            sum += self.data[i]
        sum = (0xFF - sum) + 1
        if self.data[8] != (sum & 0xFF):    # Checksum
            return False
        return True

# -----

    def interpret(self):
        co2 = (self.data[2] << 8) | self.data[3]
        self.value = co2

        self._remove_data(self.packet_size)
        return co2

#######
