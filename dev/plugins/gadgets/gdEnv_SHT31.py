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

EZPID = 'gdSHT31'
PTYPE = PT_SENSOR
PNAME = '@TEST Env.TH - SHT31 - Temp. Humidity Sensor (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'SHT31',
            'ENABLE':False,
            'TIMER':5,
            'PORT':'1',
            'ADDR':'44',
            # instance specific params
            'RespVarT':'Temperature',
            'RespVarH':'Humidity',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        # set to cyclic measurement
        self._i2c.write_buffer([0x22, 0x36])

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
        return ('44 (ADDR-GND)', '45 (ADDR-VCC)')

# -----

    def timer(self, prepare:bool):
        if not self._i2c:
            return

        try:
            name_t = self.param['RespVarT']
            name_h = self.param['RespVarH']
            if name_t or name_h:
                self._i2c.write_buffer([0xE0, 0x00])
                data = self._i2c.read_buffer(6)
                #TODO Checksum data[2] data[5]
                #print(data)
                if name_t:
                    t = ((data[0] << 8) | data[1]) / (65535/175) - 45
                    Variable.set(name_t, t)
                if name_h:
                    h = ((data[3] << 8) | data[4]) / 655.35
                    Variable.set(name_h, h)

        except Exception as e:
            print(str(e))
            self._last_error = str(e)

#######
