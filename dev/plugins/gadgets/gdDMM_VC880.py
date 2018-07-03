"""
Gadget Plugin for DMM UNI-T UT61E
Based on ???
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdDMM_VC880'
PTYPE = PT_SENSOR
PNAME = 'DMM Voltcraft VC880'
PINFO = 'Chip: ???<br>Voltcraft VC880; Voltcraft VC650BT'

#######

class PluginGadget(GS):
    """ TODO """

    def __init__(self, module):
        super().__init__(module, 39)   # 39 byte data packet
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
            self._ser.init(9600, 8, None, 1) # baud=9600 databits=8 parity=none stopbits=1
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
        if self.data[0] != 0xAB:   # Header
            return False
        if self.data[1] != 0xCD:   # Header
            return False
        if self.data[2] != 36:   # Length
            return False
        if self.data[3] != 1:   # Msg Type
            return False
        for i in range(30, 36):
            if (self.data[i] & 0xF0) != 0x30:
                return False
        return True

# -----

    def interpret(self):
        val = (self.data[6] & 0x0F)
        val *= 10
        val += (self.data[7] & 0x0F)
        val *= 10
        val += (self.data[8] & 0x0F)
        val *= 10
        val += (self.data[9] & 0x0F)
        val *= 10
        val += (self.data[10] & 0x0F)
        val *= 10
        val += (self.data[11] & 0x0F)
        val *= 10
        val += (self.data[12] & 0x0F)
        if self.data[30] & 0x04:   # neg
            val = -val

        nrange = (self.data[5] & 0x07)
        mode = (self.data[4] & 0x1F)

        unit = ''
        dec = 3
        if mode == 0x00:   # DCV
            dec = 4-nrange
            unit = 'V='
        elif mode == 0x01:   # AC+DCV
            dec = 4-nrange
            unit = 'V+'
        elif mode == 0x02:   # DCmV
            dec = 2-nrange
            unit = 'mV='
        elif mode == 0x03:   # Frequency
            dec = 3-nrange
            unit = 'Hz'
        elif mode == 0x04:   # Duty Cycle
            dec = 3-nrange
            unit = '%'
        elif mode == 0x05:   # ACV
            dec = 4-nrange
            unit = 'V~'
        elif mode == 0x06:   # Resistance
            dec = 2-nrange
            unit = 'Ohm'
        elif mode == 0x07:   # Diode
            dec = 3-nrange
            unit = 'Vdiode'
        elif mode == 0x08:   # Short Circuit
            dec = 2-nrange
            unit = 'Ohm'
        elif mode == 0x09:   # Capactiance
            dec = 5-nrange
            unit = 'uF'
        elif mode == 0x0A:   # Celsius
            dec = 1-nrange
            unit = '°C'
        elif mode == 0x0B:   # Fahrenheit
            dec = 1-nrange
            unit = '°F'
        elif mode == 0x0C:   # DCuA
            dec = 2-nrange
            unit = 'uA='
        elif mode == 0x0D:   # ACuA
            dec = 2-nrange
            unit = 'uA~'
        elif mode == 0x0E:   # DCmA
            dec = 3-nrange
            unit = 'mA='
        elif mode == 0x0F:   # ACmA
            dec = 3-nrange
            unit = 'mA~'
        elif mode == 0x10:   # DCA
            dec = 3-nrange
            unit = 'a='
        elif mode == 0x11:   # ACA
            dec = 3-nrange
            unit = 'a~'
        elif mode == 0x12:   # Low-Pass Filter
            dec = 3-nrange
            unit = '?'
        else:
            pass
        val *= GS.Pow10[-dec]

        if self.data[31] & 0x08:   # max
            unit += 'max'
        if self.data[31] & 0x04:   # min
            unit += 'min'
        if self.data[31] & 0x02:   # avg
            unit += 'avg'
        if self.data[32] & 0x04:   # OVL
            unit += 'OL'

        self.value = val
        self.unit = unit
        if dec < 0: dec = 0
        self.form = '{{:.{}f}}'.format(dec)

        self._remove_data(self.packet_size)
        return val

#######
