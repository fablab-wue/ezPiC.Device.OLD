"""
Gadget Plugin for Env. Si7021
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdDHT12'
PTYPE = PT_SENSOR
PNAME = '@WORK Env.TH - DHT12 - Temp. Humidity Sensor (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'DHT12',
            'ENABLE':False,
            'TIMER':5,
            'PORT':'1',
            'ADDR':'5C',
            # instance specific params
            'RespVarT':'Temperature',
            'RespVarH':'Humidity',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        Variable.set_meta(self.param['RespVarT'], '°C', '{:.1f}')
        Variable.set_meta(self.param['RespVarH'], '%', '{:.1f}')

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('5C')

# -----

    def timer(self, prepare:bool):
        name_t = self.param['RespVarT']
        name_h = self.param['RespVarH']
        if name_t or name_h:
            data = self._i2c.read_reg_buffer(self, 0, 5)
            #TODO Checksum data[4]
            print(data)
            if name_t:
                t = data[2] + data[3]/10
                Variable.set(name_t, t)
            if name_h:
                h = data[0] + data[1]/10
                Variable.set(name_h, h)

#######
