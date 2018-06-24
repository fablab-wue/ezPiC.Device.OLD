"""
Machine Plugin for Testing
"""
from com.Globals import *

import random

import dev.M as M
import dev.Machine as Machine

#######
# Globals:

MAPID = 'maTestM'
PTYPE = PT_MACHINE
PNAME = 'Readable Name M'
PINFO = '???'

#######

class PluginMachine(Machine.PluginMachineBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # instance specific params
            'i2c_enable':False,
            'i2c_pin_scl':None,
            'i2c_pin_sda':None,
            'i2c_status':'',
            'abc':123,
            'xyz':456,
            }
        self._pin_scl = None
        self._pin_sda = None
        self._i2c = None

# -----

    def init(self):
        super().init()
        try:
            self._pin_scl = machine.Pin(self.param['i2c_pin_scl'], machine.Pin.IN)
            self._pin_sda = machine.Pin(self.param['i2c_pin_sda'], machine.Pin.IN)
            self._i2c = machine.I2C(scl=self._pin_scl, sda=self._pin_sda, freq=400000)
        except:
            self._i2c = None
            pass
        M.I2C = self._i2c

# -----

    def exit(self):
        super().exit()
        if self._i2c:
            try:
                self._i2c.deinit()
                self._i2c = None
            except:
                pass
        M.I2C = self._i2c

#######
