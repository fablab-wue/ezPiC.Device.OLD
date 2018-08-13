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
            'TrigVar':'MCP4725.out',
            'MaxVal':'4095',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        self._scale = 0xFFF / float(self.param['MaxVal'])

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
        name = self.param['TrigVar']
        if name and name in news:
            val = Variable.get(name)
            if type(val) == str:
                val = float(val)
            val = int(val * self._scale + 0.5)
            if val < 0: val = 0
            if val > 0xFFF: val = 0xFFF
            data = [((val >> 8) & 0x0F), (val & 0xFF)]
            self._i2c.write_buffer(data)

#######
