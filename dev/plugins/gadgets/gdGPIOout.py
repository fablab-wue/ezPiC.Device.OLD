"""
Gadget Plugin for GPIO output
"""
from com.Globals import *

import dev.Gadget as Gadget
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdGPIOout'
PNAME = 'GPIO Output'
PINFO = 'Use GPIOs as Output triggered by Variables'

#######

class PluginGadget(Gadget.PluginGadgetBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'A',
            'ENABLE':False,
            'TIMER':0,
            # instance specific params
            'out_key':'TimeSwitchOut',
            'out_val_0':'0 off OFF',
            'out_val_1':'1 on ON',
            'gpio':'',
            }
        self._pin = None

# -----

    def init(self):
        super().init()

        key = self.param['out_key']
        out = self._get_variable(key)
        id = self.param['gpio']

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
            key = self.param['out_key']
            if key in news:
                out = self._get_variable(key)

                if self._pin:
                    self._pin.set(out)
        except:
            pass

# =====

    def _get_variable(self, key):
        out = 0
        val = str(Variable.get(key))

        if self.param['out_val_0'] and self.param['out_val_0'].find(val) >= 0:
            out = 0
        if self.param['out_val_1'] and self.param['out_val_1'].find(val) >= 0:
            out = 1

        return out

#######
