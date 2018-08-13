"""
Gadget Plugin for 
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdOPT3001'
PTYPE = PT_SENSOR | PT_ACTUATOR
PNAME = '@WORK ALS - OPT3001 - Luminosity (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'OPT3001',
            'ENABLE':False,
            'TIMER':3,
            'PORT':'1',
            'ADDR':'44',
            # instance specific params
            'RespVar':'OPT3001.lum',
            }

# -----

    def init(self):
        super().init()

        #if self._i2c and self.param['InitVal']:
        self._i2c.write_reg_buffer(1, [0xCE, 0x10])
        self._i2c.write_byte(0)

        Variable.set_meta(self.param['RespVar'], 'Lux', '{:.2f}')

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('44 (ADDR-GND)', '45 (ADDR-VDD)', '46 (ADDR-SDA)', '47 (ADDR-SCL)')

# -----

    def timer(self, prepare:bool):
        name = self.param['RespVar']
        if name:
            #data = self._i2c.read_reg_buffer(0, 2)
            data = self._i2c.read_buffer(2)
            e = (data[0] >> 4) & 0x0F
            m = ((data[0] & 0x0F) << 8) | data[1]
            val = 0.01 * (1 << e) * m
            print(val)
            Variable.set(name, val)

#######
