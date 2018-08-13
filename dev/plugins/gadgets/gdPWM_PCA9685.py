"""
Gadget Plugin for 16xPWM PCA9685
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdPCA9685'
PTYPE = PT_ACTUATOR
PNAME = '@WORK PWM - PCA9685 - 16-Ch 12-Bit PWM (I2C)'

INIT_SEQUENCE = (
    (0x00, 0x30),  # Mode1 = AI SLEEP
    (0x01, 0x04),  # Mode2 = OUTDRV
    (0xFE, 30),    # PRE_SCALE = 200Hz
    #(0xFE, 121),   # PRE_SCALE = 50Hz
    (0x00, 0x20),  # Mode1 = AI
)

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'PCA9685',
            'ENABLE':False,
            'TIMER':0,
            'PORT':'1',
            'ADDR':'7F',
            # instance specific params
            'Mode':'LED',   # 0=LED 1=LED-Gamma 2=RC-Servo
            'Active':'H',   # 'L'=Low-Active 'H'=High-Active
            'MaxVal':'100',
            'TrigVar0':'PWM-0',
            'TrigVar1':'PWM-1',
            'TrigVar2':'PWM-2',
            'TrigVar3':'PWM-3',
            'TrigVar4':'PWM-4',
            'TrigVar5':'PWM-5',
            'TrigVar6':'PWM-6',
            'TrigVar7':'PWM-7',
            'TrigVar8':'PWM-8',
            'TrigVar9':'PWM-9',
            'TrigVarA':'PWM-A',
            'TrigVarB':'PWM-B',
            'TrigVarC':'PWM-C',
            'TrigVarD':'PWM-D',
            'TrigVarE':'PWM-E',
            'TrigVarF':'PWM-F',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        for reg, val in INIT_SEQUENCE:
            self._i2c.write_reg_byte(reg, val)

        if self.param['Mode'].upper().startswith('RC'):
            self._offset = 819
            self._scale = 819 / float(self.param['MaxVal'])
        else:   # LED
            self._offset = 0
            self._scale = 4096 / float(self.param['MaxVal'])

        self._gamma = self.param['Mode'].upper().endswith('GAMMA')

        for i in range(16):
            self._set_val(i, 0)

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', )

# -----

    def variables(self, news:dict):
        for i, key in enumerate(
            'TrigVar0',
            'TrigVar1',
            'TrigVar2',
            'TrigVar3',
            'TrigVar4',
            'TrigVar5',
            'TrigVar6',
            'TrigVar7',
            'TrigVar8',
            'TrigVar9',
            'TrigVarA',
            'TrigVarB',
            'TrigVarC',
            'TrigVarD',
            'TrigVarE',
            'TrigVarF',
            ):
            name = self.param[key]
            if name and name in news:
                val = Variable.get(name)
                if type(val) == list:
                    for ii, subval in enumerate(val, i):
                        self._set_val(ii, subval)
                else:
                    self._set_val(i, val)

# =====

    def _set_val(self, i, val):
        i &= 0xF
        if type(val) == str:
            val = float(val)
        val = val * self._scale + self._offset
        if self._gamma:
            val /= 0x1000
            val *= val
            val *= 0x1000

        val = int(val + 0.5)
        if self.param['Active'] == 'L':
            val = 0x1000 - val
        if val <= 0:
            data = [0, i, 0, i | 0x10]
        elif val >= 0x1000:
            data = [0, i | 0x10, 0, i]
        else:
            data = [0, i, (val & 0xFF), ((val >> 8 + i) & 0x0F) ]
        self._i2c.write_reg_buffer(6 + i<<2, data)

#######
