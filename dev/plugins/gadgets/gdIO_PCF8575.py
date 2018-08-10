"""
Gadget Plugin for GPIO output
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdPCF8575'
PTYPE = PT_SENSOR | PT_ACTUATOR
PNAME = '@WORK IO - PCF8575 - 16-Bit Port Expander (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'PCF8575',
            'ENABLE':False,
            'TIMER':0.1,
            'PORT':'1',
            'ADDR':'20',
            # instance specific params
            'InitVal':'0xFFFF',
            'TrigVar':'PCF8575.out',
            'RespVar':'PCF8575.in',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        if self._i2c and self.param['InitVal']:
            val = int(self.param['InitVal'], 0) & 0xFFFF
            self._i2c.write_buffer([val & 0xFF, (val >> 8) & 0xFF])

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('20 (Default)', '21', '22', '23', '24', '25', '26', '27')

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
                if 0 <= val <= 0xFFFF:
                    self._i2c.write_buffer([val & 0xFF, (val >> 8) & 0xFF])

        except Exception as e:
            print(str(e))
            self._last_error = str(e)

# -----

    def timer(self, prepare:bool):
        if not self._i2c:
            return

        try:
            name = self.param['RespVar']
            if name:
                data = self._i2c.read_buffer(2)
                val = (data[1] << 8) | data[0]
                #print(val)
                if val != self._last_val:
                    self._last_val = val
                    Variable.set(name, val)

        except Exception as e:
            print(str(e))
            self._last_error = str(e)

#######
