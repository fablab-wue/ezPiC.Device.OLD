"""
TODO
"""
from com.Globals import *

import dev.Gadget as Gadget
#import dev.Variable as Variable
import dev.Machine as Machine


class PluginGadgetI2C(Gadget.PluginGadgetBase):
    """ TODO """
    Pow10 = { -10:0.0000000001, -9:0.000000001, -8:0.00000001, -7:0.0000001, -6:0.000001, -5:0.00001, -4:0.0001, -3:0.001, -2:0.01, -1:0.1, 0:1.0, 1:10.0, 2:100.0, 3:1000.0, 4:10000.0, 5:100000.0, 6:1000000.0, 7:10000000.0, 8:100000000.0, 9:1000000000.0, 10:10000000000.0 }

    def __init__(self, module):
        super().__init__(module)
        self._i2c = None
        self._addr = None
        
        self.value = 0.0
        self.unit = ''
        self.form = ''

# -----

    def init(self):
        super().init()

        if not self.param['ENABLE']:
            return

        try:
            id = self.param['PORT']
            err, ret = Machine.get_handler_instance('I2C', id)

            if not err:
                self._i2c = ret
                self._addr = int(self.param['ADDR'].split(' ', 1)[0], 16)
            else:
                self._i2c = None

        except Exception as e:
            self._last_error = str(e)
            self._i2c = None

# -----

    def exit(self):
        super().exit()

        if self._i2c:
            self._i2c.deinit()
            self._i2c = None

# -----

    def get_features(self):
        features = {}
        err, ret = Machine.get_features('I2C')
        if not err:
            features['Ports'] = ret

        if self._last_error:
            features['ERROR'] = self._last_error
            self._last_error = None

        features['Addrs'] = self.get_addrs()
        features['PNAME'] = self.module.PNAME
        return features

# =====

    def get_addrs(self):
        return []


#######
