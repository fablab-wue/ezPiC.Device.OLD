"""
https://sigrok.org/wiki/Multimeter_comparison
https://files.elv.com/Assets/Produkte/6/639/63997/Downloads/63997_Mastech_MS8050_Data_Format.pdf

HoldPeak HP-90K USB
FS9721 - 14-byte LCD
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdDMM_MT8'
PTYPE = PT_SENSOR
PNAME = 'DMM - Mastech MS8050 (8 Byte)'

#######

class PluginGadget(GS):
    """ TODO """

    def __init__(self, module):
        super().__init__(module, 8)   # 8 byte data packet
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
            self._ser.init(2400, 8, 0, 1) # baud=2400 databits=8 parity=even stopbits=1
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
        if (self.data[0] & 0xF0) != 0xA0:   # 1010xxxx
            return False
        for i in range(1,8):
            if (self.data[i] & 0x80) != 0x00:   # 0xxxxxxx
                return False
        return True

# -----

    def interpret(self):
        val = (self.data[3] & 0x0F)
        val *= 10
        val += (self.data[4] & 0x0F)
        val *= 10
        val += (self.data[5] & 0x0F)
        val *= 10
        val += (self.data[6] & 0x0F)
        val *= 10
        val += (self.data[7] & 0x0F)
        if self.data[2] & 0x20:   # neg
            val = -val

        nrange = (self.data[0] & 0x0F)
        mode = (self.data[1] & 0x1F)

        unit = ''
        dec = 4
        if mode == 0x00:   # ACV
            dec = 4-nrange
            unit = 'V~'
        elif mode == 0x01:   # dBm
            dec = 2
            unit = 'dBm'
        elif mode == 0x02:   # DCV
            dec = 4-nrange
            unit = 'V='
        elif mode == 0x03:   # DCV+ACV
            dec = 4-nrange
            unit = 'V+'
        elif mode == 0x04:   # DCmV
            dec = 4-nrange
            unit = 'mV='
        elif mode == 0x05:   # ACmV
            dec = 4-nrange
            unit = 'mV~'
        elif mode == 0x06:   # DCV+ACV
            dec = 4-nrange
            unit = 'mV+'
        elif mode == 0x07:   # Hz
            dec = 3-nrange
            unit = 'Hz'
        elif mode == 0x08:   # Duty
            dec = 2
            unit = '%'
        elif mode == 0x09:   # Ohm
            dec = 2-nrange
            unit = 'Ohm'
        elif mode == 0x0A:   # Continuity
            dec = 2
            unit = 'Ohm'
        elif mode == 0x0B:   # Capacitance
            dec = 5-nrange
            unit = 'uF'
        elif mode == 0x0C:   # DCuA
            dec = 2-nrange
            unit = 'uA='
        elif mode == 0x0D:   # ACuA
            dec = 2-nrange
            unit = 'uA~'
        elif mode == 0x0E:   # DCuA-ACuA
            dec = 2-nrange
            unit = 'uA+'
        elif mode == 0x0F:   # DCmA
            dec = 3-nrange
            unit = 'mA='
        elif mode == 0x10:   # ACmA
            dec = 3-nrange
            unit = 'mA~'
        elif mode == 0x11:   # DCmA+ACmA
            dec = 3-nrange
            unit = 'mA+'
        elif mode == 0x012:   # DCA
            dec = 4-nrange
            unit = 'A='
        elif mode == 0x13:   # ACA
            dec = 4-nrange
            unit = 'A~'
        elif mode == 0x14:   # DCA+ACA
            dec = 4-nrange
            unit = 'A+'
        else:
            pass

        val *= GS.Pow10[-dec]

        #if self.data[10] & 0x08:   # DC
        #    unit += '='
        #if self.data[10] & 0x04:   # AC
        #    unit += '~'
        if self.data[2] & 0x01:   # max
            unit += 'max'
        if self.data[2] & 0x02:   # min
            unit += 'min'
        if self.data[1] & 0x20:   # OVL
            unit += 'OL'

        self.value = val
        self.unit = unit
        if dec < 0: dec = 0
        self.form = '{{:.{}f}}'.format(dec)

        self._remove_data(self.packet_size)
        return val

#######
