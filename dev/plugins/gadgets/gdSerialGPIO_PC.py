"""
Gadget Plugin for GPIO output
"""
import serial
from serial.tools.list_ports import comports

from com.Globals import *

import dev.Gadget as Gadget
import dev.Variable as Variable

#######
# Globals:

GDPID = 'SerialGPIO'
PNAME = 'PC Serial GPIO'
PINFO = 'GPIO with USB-Serial-Adapter at Windows/Linux'

#######

class PluginGadget(Gadget.PluginGadgetBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'name':'SerialGPIO',
            'enable':False,
            'timer':0,
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

        try:
            self._ser = serial.Serial('COM17')
            self._ser.baudrate = 115200
            self._ser.timeout = 2.5

            self._ser.in_waiting

            self._ser.write(b'hello')

            self._ser.is_open
            cts = self._ser.cts
            dsr = self._ser.dsr
            ri = self._ser.ri
            cd = self._ser.cd


            key = self.param['out_key']
            out = self._get_variable(key)
            id = self.param['gpio']

            self._pin = None
        except:
            pass

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        ports = []
        for n, (port_id, port_desc, hwid) in enumerate(sorted(comports()), 1):
            port_str = port_id + ' - ' + port_desc
            ports.append(port_str)

        features = {'ports':ports}
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
