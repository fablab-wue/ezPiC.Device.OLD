"""
Gadget Plugin for DMM UNI-T UT61B/C/D
Based on https://www-user.tu-chemnitz.de/~heha/hs/UNI-T/UT61BCD.LOG
https://sigrok.org/wiki/Multimeter_ICs/Cyrustek_ES519xx

https://sigrok.org/wiki/Multimeter_ICs#Fortune_Semiconductor_FS9721_LP3


FS9721 - 14-byte LCD
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdDMM_LCD14'
PTYPE = PT_SENSOR
PNAME = 'DMM FS9721 (14 Byte LCD)'
PINFO = 'Chip: FS9721<br>HoldPeak HP-90K USB; Voltcraft VC 820; Vichy VC99<br>Note: Press PC-Link button to start tranmition'

#######

class PluginGadget(GS):
    """ TODO """

    def __init__(self, module):
        super().__init__(module, 14)   # 14 byte data packet
        self.param = {
            # must be params
            'NAME':PNAME,
            'ENABLE':False,
            'TIMER':0.1,
            'PORT':'COM5',
            # instance specific params
            'RespVar':'DMM',
            }

# -----

    def init(self):
        super().init()

        if self._ser:
            self._ser.init(2400, 8, None, 1) # baud=2400 databits=0 parity=none stopbits=1
            self._ser.set_dtr(True)    # DTR-pin to +
            self._ser.set_rts(False)   # RTS-pin to -

# -----

    def exit(self):
        super().exit()

# -----

    def timer(self, prepare:bool):
        while self.process():
            print(self.value, self.unit, self.form)
            key = self.param['RespVar']
            source = self.param['NAME']
            Variable.set(key, self.value, source, self.unit, self.form)

# =====

    def is_valid(self):
        for i in range(14):
            if (self.data[i] & 0xF0) != ((i+1)<<4):
                return False
        return True

# -----
    def interpret(self):
        segs = {0:0, 125:0, 5:1, 91: 2, 31:3, 39:4, 62:5, 126:6, 21:7, 127:8, 63:9, 104:9999}
        val = 0
        seg = (self.data[1] & 0x07)<<4 | (self.data[2] & 0x0F)
        val += segs[seg]
        val *= 10
        seg = (self.data[3] & 0x07)<<4 | (self.data[4] & 0x0F)
        val += segs[seg]
        val *= 10
        seg = (self.data[5] & 0x07)<<4 | (self.data[6] & 0x0F)
        val += segs[seg]
        val *= 10
        seg = (self.data[7] & 0x07)<<4 | (self.data[8] & 0x0F)
        val += segs[seg]

        if self.data[1] & 0x08:   # neg
            val = -val

        if self.data[3] & 0x08:     # 0.000
            dec = 3
        elif self.data[5] & 0x08:   # 00.00
            dec = 2
        elif self.data[7] & 0x08:   # 000.0
            dec = 1
        else:                       # 0000
            dec = 0
        val *= GS.Pow10[-dec]

        unit = ''

        if self.data[9] & 0x08:   # u
            unit += 'u'
        if self.data[9] & 0x04:   # n
            unit += 'n'
        if self.data[9] & 0x02:   # k
            unit += 'k'
        if self.data[9] & 0x01:   # Diode
            unit += 'Diode'
        if self.data[10] & 0x08:  # m
            unit += 'm'
        if self.data[10] & 0x04:  # %
            unit += '%'
        if self.data[10] & 0x02:  # M
            unit += 'M'
        if self.data[10] & 0x01:  # Beep
            unit += 'Beep'
        if self.data[11] & 0x08:  # F
            unit += 'F'
        if self.data[11] & 0x04:  # Ohm
            unit += 'Ohm'
        if self.data[12] & 0x08:  # A
            unit += 'A'
        if self.data[12] & 0x04:  # V
            unit += 'V'
        if self.data[12] & 0x02:  # Hz
            unit += 'Hz'

        if self.data[0] & 0x08:   # AC
            unit += '~'
        if self.data[0] & 0x04:   # DC
            unit += '='

        self.value = val
        self.unit = unit
        if dec < 0: dec = 0
        self.form = '{{:.{}f}}'.format(dec)

        self._remove_data(self.packet_size)
        return val

#######
