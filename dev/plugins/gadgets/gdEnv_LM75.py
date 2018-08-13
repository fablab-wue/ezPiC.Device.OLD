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

EZPID = 'gdLM75'
PTYPE = PT_SENSOR
PNAME = '@WORK Env.T - LM75 - Temp. Sensor (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'LM75',
            'ENABLE':False,
            'TIMER':3,
            'PORT':'1',
            'ADDR':'48',
            # instance specific params
            'RespVar':'LM75.T',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        #if self._i2c and self.param['InitVal']:
        self._i2c.write_byte(0)

        Variable.set_meta(self.param['RespVar'], '°C', '{:.1f}')

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('48 (Default)', '49', '4A', '4B', '4C', '4D', '4E', '4F')

# -----

    def variables(self, news:dict):
        if not self._i2c:
            return

        try:
            name = self.param['TrigVar']
            if name and name in news:
                val = Variable.get(name)
                if type(val) == str:
                    val = int(val, 0)
                if 0 <= val <= 255:
                    self._i2c.write_byte(val)

        except Exception as e:
            print(str(e))
            self._last_error = str(e)

# -----

    def timer(self, prepare:bool):
        name = self.param['RespVar']
        if name:
            data = self._i2c.read_buffer(2)
            val = ((data[0] & 0xFF) << 3) | ((data[1] & 0x01) >> 5)
            if val >= 0x400:
                val -= 0x800
            val /= 8
            print(val)
            Variable.set(name, val)

#######
