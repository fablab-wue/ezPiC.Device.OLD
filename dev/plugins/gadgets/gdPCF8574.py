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

EZPID = 'gdPCF8574'
PTYPE = PT_SENSOR | PT_ACTUATOR
PNAME = 'IO - PCF8574 Port Expander (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'PCF8574',
            'ENABLE':False,
            'TIMER':2.1,
            'PORT':'1',
            'ADDR':'3A',
            # instance specific params
            'InitVal':'0xFF',
            'TrigVar':'I2C.T',
            'RespVar':'I2C.R',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        if self._i2c and self.param['InitVal']:
            self._i2c.write_byte(int(self.param['InitVal'], 0))

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('20 (Default)', '21', '22', '23', '24', '25', '26', '27', '38 (Default Type A)', '39', '3A', '3B', '3C', '3D', '3E', '3F')

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
        if not self._i2c:
            return

        try:
            name = self.param['RespVar']
            if name:
                val = self._i2c.read_byte()
                #print(val)
                if val != self._last_val:
                    self._last_val = val
                    Variable.set(name, val)

        except Exception as e:
            print(str(e))
            self._last_error = str(e)

#######
