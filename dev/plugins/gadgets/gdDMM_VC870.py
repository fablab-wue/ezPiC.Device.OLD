"""
Gadget Plugin for DMM VC870
Based on ???

"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdDMM_VC870'
PTYPE = PT_SENSOR
PNAME = 'DMM Voltcraft VC870'
PINFO = 'Chip: ???<br>Voltcraft VC870'

#######

class PluginGadget(GS):
    """ TODO """

    def __init__(self, module):
        super().__init__(module, 23)   # 23 byte data packet
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
        if self.data[22] != 0x0A:   # '\n'
            return False
        if self.data[21] != 0x0D:   # '\r'
            return False
        for i in range(21):
            if (self.data[i] & 0xF0) != 0x30:
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
        if self.data[15] & 0x04:   # neg
            val = -val

        nrange = (self.data[2] & 0x07)
        fc = (self.data[0] & 0x0F)
        fsc = (self.data[1] & 0x0F)

        unit = ''
        dec = 3
        if fc == 0 and fsc == 0:   # DCV
            dec = 4-nrange
            unit = 'V='
        if fc == 0 and fsc == 1:   # ACV
            dec = 3-nrange
            unit = 'V~'
        elif fc == 1 and fsc == 0:   # mV
            dec = 2-nrange
            unit = 'mV='
        elif fc == 1 and fsc == 1:   # Celcius
            dec = 1-nrange
            unit = '°C'
        elif fc == 2:   # Ohm
            dec = 2-nrange
            if fsc == 0:   # Resistance
                unit = 'Ohm'
            else:   # Short-circuit
                unit = 'Ohm'
        elif fc == 3:   # Capacitance
            dec = nrange-6
            unit = 'uF'
        elif fc == 4:   # Diode
            dec = 4-nrange
            unit = 'Vdiode'
        elif fc == 5 and fsc == 0:   # Frequency
            dec = 3-nrange
            unit = 'Hz'
        elif fc == 5 and fsc == 1:   # 4-20mA
            dec = 3-nrange
            unit = '%'
        elif fc == 6 and fsc == 0:   # DCuA
            dec = 2-nrange
            unit = 'uA='
        elif fc == 6 and fsc == 1:   # ACuA
            dec = 1-nrange
            unit = 'uA~'
        elif fc == 7 and fsc == 0:   # DCmA
            dec = 3-nrange
            unit = 'mA='
        elif fc == 7 and fsc == 1:   # ACmA
            dec = 2-nrange
            unit = 'mA~'
        elif fc == 8 and fsc == 0:   # DCA
            dec = 3-nrange
            unit = 'A='
        elif fc == 8 and fsc == 1:   # ACA
            dec = 2-nrange
            unit = 'A~'
        elif fc == 9 and fsc == 0:   # Active Power
            dec = 1-nrange
            unit = 'W'
        elif fc == 9 and fsc == 1:   # Power Factor / Cos Phi
            dec = 3-nrange
            unit = '°'
        elif fc == 9 and fsc == 2:   # Voltage eff.
            dec = 1-nrange
            unit = 'Veff'
        else:
            pass
        val *= GS.Pow10[-dec]

        if self.data[16] & 0x08:   # max
            unit += 'max'
        if self.data[16] & 0x04:   # min
            unit += 'min'
        if self.data[15] & 0x01:   # OVL
            unit += 'OL'
        if self.data[17] & 0x04:   # UL
            unit += 'UL'

        self.value = val
        self.unit = unit
        if dec < 0: dec = 0
        self.form = '{{:.{}f}}'.format(dec)

        self._remove_data(self.packet_size)
        return val

#######
