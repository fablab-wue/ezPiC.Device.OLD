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
PNAME = '@PLAN PWM - PCA9685 - 16-Ch 12-Bit PWM (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'PCA9685',
            'ENABLE':False,
            'TIMER':2.1,
            'PORT':'1',
            'ADDR':'7F',
            # instance specific params
            'Mode':'0',   # RC-Servo, LED, Gamma, 0...1
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
        return ('70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', )

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
