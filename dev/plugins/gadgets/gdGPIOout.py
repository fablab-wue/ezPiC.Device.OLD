"""
Gadget Plugin for Port output
"""
from com.Globals import *

import dev.Gadget as Gadget
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdGPIOout'
PTYPE = PT_ACTUATOR
PNAME = 'IO - GPIO Port Output'

#######

class PluginGadget(Gadget.PluginGadgetBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':PNAME,
            'ENABLE':False,
            'TIMER':0,
            # instance specific params
            'TrigVar':'TimeSwitchOut',
            'TrigVals1':'1 on ON',
            'Port':'',
            }
        self._pin = None

# -----

    def init(self):
        super().init()

        key = self.param['TrigVar']
        out = self._get_variable(key)
        id = self.param['Port']

        err, ret = Machine.get_handler_instance('PIN_IO', id)
        if not err:
            self._pin = ret
            self._pin.mode(self._pin.OUT)
            self._pin.set(out)
        else:
            self._pin = None

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        features = {}
        err, ret = Machine.get_features('PIN_O')
        if not err:
            features['PIN_O'] = ret
        return features

# -----

    def variables(self, news:dict):
        try:
            key = self.param['TrigVar']
            if key in news:
                out = self._get_variable(key)

                if self._pin:
                    self._pin.set(out)
        except:
            pass

# =====

    def _get_variable(self, key):
        val = str(Variable.get(key))

        if self.param['TrigVals1'] and self.param['TrigVals1'].find(val) >= 0:
            return True

        return False

#######
