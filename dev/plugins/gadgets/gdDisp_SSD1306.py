"""
Gadget Plugin for SSD1306
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdSSD1306'
PTYPE = PT_SENSOR | PT_ACTUATOR
PNAME = '@PLAN Disp.Text - SSD1306, SSD1309 - OLED Display (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'SSD1306',
            'ENABLE':False,
            'TIMER':3,
            'PORT':'1',
            'ADDR':'3C',
            # instance specific params
            'Text':'Text',
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
        return ('3C', '3D', '78', '7A')

# -----

    def variables(self, news:dict):
        name = self.param['TrigVar']
        if name and name in news:
            val = Variable.get(name)
            if type(val) == str:
                val = int(val, 0)
            if 0 <= val <= 255:
                self._i2c.write_byte(val)

# -----

    def timer(self, prepare:bool):
        name = self.param['RespVar']
        if name:
            val = self._i2c.read_byte()
            print(val)
            if val != self._last_val:
                self._last_val = val
                Variable.set(name, val)

#######
