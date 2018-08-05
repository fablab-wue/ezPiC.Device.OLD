"""
Gadget Plugin for Char LCD
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdCharLCD'
PTYPE = PT_SENSOR | PT_ACTUATOR
PNAME = 'Disp - Char.LCD (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'CharLCD',
            'ENABLE':False,
            'TIMER':2.1,
            'PORT':'1',
            'ADDR':'3F',
            # instance specific params
            'Size':'2004',
            'Row0':'Text0',
            'Row1':'Text1',
            'Row2':'Text2',
            'Row3':'Text3',
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
        return ('3F')

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
                print(val)
                if val != self._last_val:
                    self._last_val = val
                    Variable.set(name, val)

        except Exception as e:
            print(str(e))
            self._last_error = str(e)

#######
