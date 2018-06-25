"""
Gadget Plugin for GPIO output
"""
from com.Globals import *

import dev.Gadget as Gadget
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdDmmMS8050'
PTYPE = PT_SENSOR
PNAME = 'DMM Mastech/ELV MS8050'
PINFO = '???'

#######

class PluginGadget(Gadget.PluginGadgetBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':PNAME,
            'ENABLE':False,
            'TIMER':0.1,
            # instance specific params
            'Port':'',
            'RespVar':'DMM',
            }
        self._ser = None

# -----

    def init(self):
        super().init()

        try:
            #out = self._get_variable(key)
            id = self.param['Port']

            err, ret = Machine.get_handler_instance('UART', id)
            if not err:
                self._ser = ret
                self._ser.init(2400, 8, 0, 1)
            else:
                self._pin = None
        except Exception as e:
            self._pin = None

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        features = {}
        err, ret = Machine.get_features('UART')
        if not err:
            features['UART'] = ret
        return features

# -----

    def timer(self, prepare:bool):
        try:
            name = self.param['RespVar']
        except:
            pass

# =====

#######
