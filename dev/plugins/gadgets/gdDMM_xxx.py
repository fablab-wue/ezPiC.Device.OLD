"""
Gadget Plugin for DMM UNI-T UT61B/C/D
Based on https://www-user.tu-chemnitz.de/~heha/hs/UNI-T/UT61BCD.LOG
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdDMM_UT61BCD'
PTYPE = PT_SENSOR
PNAME = 'DMM UT61B/C/D'
PINFO = 'Chip: FS9721<br>UNI-T UT61B/C/D; HoldPeak HP-90K; Vichy VC99<br>Note: Press REL button for 3 sec to start tranmition'

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
            'PORT':'COM22',
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
        if self.data[13] != 0x0A:   # '\n'
            return False
        if self.data[12] != 0x0D:   # '\r'
            return False
        if (self.data[0] & 0xF0) != 0x20:   #
            return False
        for i in range(1, 5):
            if (self.data[i] & 0xF0) != 0x30:
                return False
        return True

# -----

    def interpret(self):
        val = (self.data[1] & 0x0F)
        val *= 10
        val += (self.data[2] & 0x0F)
        val *= 10
        val += (self.data[3] & 0x0F)
        val *= 10
        val += (self.data[4] & 0x0F)
        if self.data[0] & 0x02:   # neg
            val = -val

        nrange = (self.data[6] & 0x07)
        if nrange == 1:
            dec = 3
        elif nrange == 2:
            dec = 2
        elif nrange == 4:
            dec = 1
        else:
            dec = 0
        val *= GS.Pow10[-dec]

        unit = ''

        if self.data[8] & 0x02:   # n
            unit += 'n'
        if self.data[9] & 0x80:   # u
            unit += 'u'
        if self.data[9] & 0x40:   # m
            unit += 'm'
        if self.data[9] & 0x20:   # k
            unit += 'k'
        if self.data[9] & 0x10:   # M
            unit += 'M'
        if self.data[9] & 0x08:   # Beep
            unit += 'Beep'
        if self.data[9] & 0x04:   # Diode
            unit += 'Diode'
        if self.data[9] & 0x02:   # %
            unit += '%'
        if self.data[10] & 0x80:   # V
            unit += 'V'
        if self.data[10] & 0x40:   # A
            unit += 'A'
        if self.data[10] & 0x20:   # Ohm
            unit += 'Ohm'
        if self.data[10] & 0x08:   # Hz
            unit += 'Hz'
        if self.data[10] & 0x04:   # F
            unit += 'F'
        if self.data[10] & 0x02:   # °C
            unit += '°C'
        if self.data[10] & 0x01:   # °F
            unit += '°F'

        if self.data[7] & 0x10:   # DC
            unit += '='
        if self.data[7] & 0x08:   # AC
            unit += '~'

        if self.data[8] & 0x20:   # max
            unit += 'max'
        if self.data[8] & 0x10:   # min
            unit += 'min'

        self.value = val
        self.unit = unit
        if dec < 0: dec = 0
        self.form = '{{:.{}f}}'.format(dec)

        self._remove_data(self.packet_size)
        return val

#######
