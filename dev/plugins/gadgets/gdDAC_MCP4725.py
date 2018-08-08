"""
Gadget Plugin for DAC MCP4725
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdMCP4725'
PTYPE = PT_ACTUATOR
PNAME = '@WORK DAC - MCP4725 - 1-Ch 12-Bit DAC (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'MCP4725',
            'ENABLE':False,
            'TIMER':0,
            'PORT':'1',
            'ADDR':'60',
            # instance specific params
            'TrigVar':'DAC',
            'MaxVal':'4095',
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
        return ('60', '61')

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
                if 0 <= val <= 4095:
                    data = [((val >> 8) & 0x0F), (val & 0xFF)]
                    self._i2c.write_buffer(data)

        except Exception as e:
            print(str(e))
            self._last_error = str(e)

#######
