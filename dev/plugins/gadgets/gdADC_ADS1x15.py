"""
Gadget Plugin for ADC ADS1x15
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdADS1x15'
PTYPE = PT_SENSOR
PNAME = '@PLAN ADC - ADS1015, ADS1115 - 4-Ch 12/16-Bit ADC (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'ADS1x15',
            'ENABLE':False,
            'TIMER':2.1,
            'PORT':'1',
            'ADDR':'48',
            # instance specific params
            'RespVar':'ADS1x15.value',
            #'RespVar0':'Channel0',
            #'RespVar1':'Channel1',
            #'RespVar2':'Channel2',
            #'RespVar3':'Channel3',
            'PGA':'0',
            'Mux':'0',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        test = self._i2c.read_reg_word(1, little_endian=False, signed=False)

        mux = 0x4
        pga = 0x1
        sps = 0x0
        data = (mux << 12) | (pga << 9) | (sps << 5)
        # MSB first
        self._i2c.write_reg_word(1, data, little_endian=False, signed=False)

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('48 (ADDR-GND)', '49 (ADDR-VDD)', '4A (ADDR-SDA)', '4B (ADDR-SCL)')

# -----

    def timer(self, prepare:bool):
        name = self.param['RespVar']
        if name:
            val = self._i2c.read_reg_word(0, little_endian=False, signed=True)
            print(val)
            Variable.set(name, val)

#######
