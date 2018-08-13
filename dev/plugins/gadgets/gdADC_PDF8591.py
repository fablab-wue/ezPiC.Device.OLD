"""
Gadget Plugin for ADC PCF8591
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdPDF8591'
PTYPE = PT_SENSOR | PT_ACTUATOR
PNAME = '@WORK ADC+DAC - PDF8591 - 4-Ch 8-Bit ADC, 1-CH 8-Bit DAC (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'PDF8591',
            'ENABLE':False,
            'TIMER':3.0,
            'PORT':'1',
            'ADDR':'48',
            # instance specific params
            'TrigVar':'PDF8591.out',
            'RespVar0':'PDF8591.Channel0',
            'RespVar1':'PDF8591.Channel1',
            'RespVar2':'PDF8591.Channel2',
            'RespVar3':'PDF8591.Channel3',
            'Mode':'0',
            'MaxVal':'255',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        self._ctrl_reg = 0x44 | ((int(self.param['Mode'], 0) & 0x03) << 4)
        self._scale = 0xFF / float(self.param['MaxVal'])

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('48', '49', '4A', '4B', '4C', '4D', '4E', '4F')

# -----

    def variables(self, news:dict):
        name = self.param['TrigVar']
        if name and name in news:
            val = Variable.get(name)
            if type(val) == str:
                val = float(val)
            val = int(val * self._scale + 0.5)
            if val < 0: val = 0
            if val > 0xFF: val = 0xFF
            self._i2c.write_reg_byte(self._ctrl_reg, val)

# -----

    def timer(self, prepare:bool):
        data = self._i2c.read_reg_buffer(self._ctrl_reg, 5)
        for i, key in enumerate(['RespVar0', 'RespVar1', 'RespVar2', 'RespVar3'], 1):
            name = self.param[key]
            if name:
                Variable.set(name, data[i])

#######
