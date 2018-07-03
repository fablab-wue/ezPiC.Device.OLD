"""
Gadget Plugin for DMM ASCII 14 Byte
Based on ???
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdDMM_M14C'
PTYPE = PT_SENSOR
PNAME = 'DMM ASCII 14 Byte C'
PINFO = 'Chip: ???<br>Metex; Voltcraft; Peaktech'

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
            'Baud':'2400',
            }

# -----

    def init(self):
        super().init()

        if self._ser:
            self._ser.init(self.param['Baud'], 7, 1, 1) # baud=19200 databits=7 parity=odd stopbits=1
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
        for i in range(13):
            if (self.data[i] & 0x80) != 0x00:
                return False
        return True

# -----

    def interpret(self):

        mode_str = data[0:2]
        val_str = data[2:9]
        unit_str = data[9:13]

        try:
            mode = mode_str.decode()
            val = float(val_str.decode())
            unit = unit_str.decode()
        except:
            s
        unit = ''
        dec = 3
        if self.data[7] & 0x08:   # % TODO
            dec = 1
            val *= GS.Pow10[-dec]
            unit = '%_'
        elif self.data[9] & 0x01:   # Hz TODO
            dec = 1
            val *= GS.Pow10[-dec]
            unit = 'Hz_'
        elif mode == 0x0:   # A
            dec = 3
            val *= GS.Pow10[-dec]
            unit = 'A'
        elif mode == 0x1:   # Diode
            dec = 2-nrange
            val *= GS.Pow10[-dec]
            unit = 'Vdiode'
        elif mode == 0x2:   # Hz
            if nrange<2:
                dec = 2-nrange
            else:
                dec = 3-nrange
            val *= GS.Pow10[-dec]
            unit = 'Hz'
        elif mode == 0x3:   # Ohm
            dec = 2-nrange
            val *= GS.Pow10[-dec]
            unit = 'Ohm'
        elif mode == 0x4:   # °C
            dec = 2-nrange
            val *= GS.Pow10[-dec]
            unit = '°C'
        elif mode == 0x5:   # Beep
            dec = 2-nrange
            val *= GS.Pow10[-dec]
            unit = 'Vbeep'
        elif mode == 0x6:   # F
            dec = 6-nrange
            val *= GS.Pow10[-dec]
            unit = 'uF'
        elif mode == 0x9:   # A
            dec = 3
            val *= GS.Pow10[-dec]
            unit = 'A'
        elif mode == 0xB:   # V
            if nrange == 4:   # mV
                dec = 5
            else:
                dec = 4-nrange
            val *= GS.Pow10[-dec]
            unit = 'V'
        elif mode == 0xD:   # uA
            dec = 2-nrange
            val *= GS.Pow10[-dec]  
            unit = 'uA'
        elif mode == 0xE:   # ADP
            dec = 2-nrange
            val *= GS.Pow10[-dec]
            unit = 'ADP'
        elif mode == 0xF:   # mA
            dec = 3-nrange
            val *= GS.Pow10[nrange-3]  
            unit = 'mA'
        else:
            pass

        if self.data[10] & 0x08:   # DC
            unit += '='
        if self.data[10] & 0x04:   # AC
            unit += '~'
        if self.data[9] & 0x04:   # max
            unit += 'max'
        if self.data[9] & 0x02:   # min
            unit += 'min'
        if self.data[7] & 0x01:   # OVL
            unit += 'OL'
        if self.data[9] & 0x08:   # UL
            unit += 'UL'

        self.value = val
        self.unit = unit
        if dec < 0: dec = 0
        self.form = '{{:.{}f}}'.format(dec)

        self._remove_data(self.packet_size)
        return val

#######
