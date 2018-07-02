"""
https://sigrok.org/wiki/Multimeter_comparison
https://files.elv.com/Assets/Produkte/6/639/63997/Downloads/63997_Mastech_MS8050_Data_Format.pdf   8Btye-Format!
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdDMM_MT14'
PTYPE = PT_SENSOR
PNAME = 'DMM Mastech MS8050 (14 Byte)'
PINFO = 'Chip: ???<br>Mastech MS8050, ELV MS8050, Sinometer MS8050<br>Note: Press yellow button for 3 sec to start tranmition'

#######

class PluginGadget(GS):
    """ TODO """

    def __init__(self, module):
        super().__init__(module, 14)   # 14 byte data packet
        self.param = {
            # must be params
            'NAME':PNAME,
            'ENABLE':False,
            'TIMER':0.05,
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
            #print(self.value, self.unit, self.form)
            key = self.param['RespVar']
            source = self.param['NAME']
            Variable.set(key, self.value, source, self.unit, self.form)

# =====

    def is_valid(self):
        if (self.data[0] & 0xF0) != 0xA0:   # 1010xxxx
            return False
        for i in range(1,9):
            if (self.data[i] & 0x80) != 0x00:   # 0xxxxxxx
                return False
        return True

# -----

    def interpret(self):
        val = (self.data[4] & 0x0F)
        val *= 10
        val += (self.data[5] & 0x0F)
        val *= 10
        val += (self.data[6] & 0x0F)
        val *= 10
        val += (self.data[7] & 0x0F)
        val *= 10
        val += (self.data[8] & 0x0F)
        if self.data[2] & 0x20:   # neg
            val = -val

        nrange = (self.data[0] & 0x0F)
        mode = (self.data[1] & 0x1F)

        #print ('Range:', nrange, 'Mode:', mode, 'Val:', val)

        unit = ''
        dec = 4
        if mode == 0:   # ACV
            dec = 4-nrange
            unit = 'V~'
            if val < 0: val = -val
        elif mode == 1:   # DCV
            dec = 4-nrange
            unit = 'V='
        elif mode == 2:   # DCV+ACV
            dec = 4-nrange
            unit = 'V+'
        elif mode == 3:   # DCmV
            dec = 3-nrange
            unit = 'mV='
        elif mode == 4:   # ACmV
            dec = 3-nrange
            unit = 'mV~'
            if val < 0: val = -val
        elif mode == 5:   # DCV+ACV
            dec = 3-nrange
            unit = 'mV+'
        elif mode == 6:   # Hz
            dec = 3-nrange
            unit = 'Hz'
        elif mode == 7:   # Diode
            dec = 4-nrange
            unit = 'V'
        elif mode == 8:   # Ohm
            dec = 2-nrange
            unit = 'Ohm'
        elif mode == 9:   # Continuity
            dec = 2
            unit = 'Ohm'
        elif mode == 10:   # Capacitance
            dec = 5-nrange
            unit = 'uF'
        elif mode == 11:   # DCuA
            dec = 2-nrange
            unit = 'uA='
        elif mode == 12:   # ACuA
            dec = 2-nrange
            unit = 'uA~'
            if val < 0: val = -val
        elif mode == 13:   # DCuA+ACuA
            dec = 2-nrange
            unit = 'uA+'
        elif mode == 14:   # DCmA
            dec = 3-nrange
            unit = 'mA='
        elif mode == 15:   # ACmA
            dec = 3-nrange
            unit = 'mA~'
            if val < 0: val = -val
        elif mode == 16:   # DCmA+ACmA
            dec = 3-nrange
            unit = 'mA+'
        elif mode == 17:   # DCA
            dec = 4-nrange
            unit = 'A='
        elif mode == 18:   # ACA
            dec = 4-nrange
            unit = 'A~'
            if val < 0: val = -val
        elif mode == 19:   # DCA+ACA
            dec = 4-nrange
            unit = 'A+'
        else:
            pass

        val *= GS.Pow10[-dec]

        if self.data[2] & 0x01:   # max
            unit += 'max'
        if self.data[2] & 0x02:   # min
            unit += 'min'
        if self.data[1] & 0x20:   # OVL
            unit += '.OL'

        self.value = val
        self.unit = unit
        if dec < 0: dec = 0
        self.form = '{{:.{}f}}'.format(dec)

        self._remove_data(self.packet_size)
        return val

#######
