"""
Gadget Plugin for SDS011 and SDS018
Based on 
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdDust_SDS01x'
PTYPE = PT_SENSOR
PNAME = 'Dust Sensor SDS011/018'
PINFO = 'Nova Fitness SDS011; SDS018'

UNIT = 'µg/m³'   #ANSI
#UNIT = 'ug/m3'   #ASCII

#######

class PluginGadget(GS):
    """ TODO """

    def __init__(self, module):
        super().__init__(module, 10)   # 10 byte data packet
        self.param = {
            # must be params
            'NAME':PNAME,
            'ENABLE':False,
            'TIMER':0,
            'PORT':'COM22',
            # instance specific params
            'RespVarPM2_5':'PM2_5',
            'RespVarPM10':'PM10',
            }

# -----

    def init(self):
        super().init()

        if self._ser:
            self._ser.init(9600, 8, None, 1) # baud=9600 databits=8 parity=none stopbits=1
            #self._ser.set_dtr(True)    # DTR-pin to +
            #self._ser.set_rts(False)   # RTS-pin to -
        Variable.set_meta(self.param['RespVarPM2_5'], UNIT, '{:.1f}')
        Variable.set_meta(self.param['RespVarPM10'], UNIT, '{:.1f}')

        self.sum_pm2_5 = 0
        self.sum_pm10 = 0
        self.sum_count = 0

# -----

    def exit(self):
        super().exit()

# -----

    def idle(self):
        while self.process():
            if self.param['TIMER'] <= 1:
                self.timer(False)

# -----

    def timer(self, prepare:bool):
        if self.sum_count:
            source = self.param['NAME']
            pm2_5 = self.sum_pm2_5 / self.sum_count * 0.1
            pm10 = self.sum_pm10 / self.sum_count * 0.1
            print(pm2_5, pm10)

            key = self.param['RespVarPM2_5']
            Variable.set(key, pm2_5, source)
            key = self.param['RespVarPM10']
            Variable.set(key, pm10, source)

            self.sum_pm2_5 = 0
            self.sum_pm10 = 0
            self.sum_count = 0

# =====

    def is_valid(self):
        if self.data[0] != 0xAA:   # Head
            return False
        if self.data[9] != 0xAB:   # Tail
            return False
        if self.data[1] != 0xC0:   # Command ID
            return False
        sum = 0
        for i in range(2, 8):
            sum += self.data[i]
        if self.data[8] != (sum & 0xFF):    # Checksum
            return False
        return True

# -----

    def interpret(self):
        pm2_5 = (self.data[3] << 8) | self.data[2]
        pm10 = (self.data[5] << 8) | self.data[4]

        self.sum_pm2_5 += pm2_5
        self.sum_pm10 += pm10
        self.sum_count += 1

        self._remove_data(self.packet_size)
        return

#######
