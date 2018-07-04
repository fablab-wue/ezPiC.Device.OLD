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
PNAME = 'DMM ASCII 14 Byte Cont.'
PINFO = 'Chip: ???<br>Metex; Voltcraft; Peaktech'

#######

class PluginGadget(GS):
    """ TODO """

    def __init__(self, module, size=14):
        super().__init__(module, size)   # 14 byte data packet
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

        mode_str = self.data[0:2]
        val_str = self.data[2:9]
        unit_str = self.data[9:13]

        try:
            mode = mode_str.decode().strip()
            val = val_str.decode().strip()
            unit = unit_str.decode().strip()
        except:
            mode = ''
            val = 0
            unit = 'OL'

        if mode.startswith('DC'):   # DC
            unit += '='
        if mode.startswith('AC'):   # AC
            unit += '~'

        self.value = val
        self.unit = unit
        #self.form = '{{:.{}f}}'.format(dec)
        self.form = None

        self._remove_data(self.packet_size)
        return val

#######
