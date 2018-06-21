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
PNAME = 'PC Serial Adapter GPIO'
PINFO = 'GPIO with USB-Serial-Adapter at Windows/Linux'

#######

class PluginGadget(Gadget.PluginGadgetBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'SerialGPIO',
            'ENABLE':False,
            'TIMER':1000,
            # instance specific params
            'Port':'',

            'TrigVarDTR':'',
            'TrigVarRTS':'',
            'TrigVarTXD':'',
            'TrigVals1':'1 on ON',

            'RespVarDSR':'',
            'RespVarCTS':'',
            'RespVarRI':'',
            'RespVarCD':'',
            'RespVarRXD':'',
            'RespVal0':'0',
            'RespVal1':'1',
            }
        self._ser = None
        self._last_error = None
        self._reset_state()

# -----

    def init(self):
        self.param['TIMER'] = 0.1
        super().init()
        if not self.param['ENABLE']:
            return

        try:
            self._reset_state()
            port = self.param['Port']
            if not port:
                return
            port = port.strip().split(' ', 1)[0]
            self._ser = serial.Serial(port)
            self._ser.dtr = False
            self._ser.rts = False

        except Exception() as e:
            self._last_error = str(e)
            pass

# -----

    def exit(self):
        super().exit()

        if self._ser:
            self._ser.close()
            self._ser = None

# -----

    def get_features(self):
        ports = []
        for n, (port_id, port_desc, hwid) in enumerate(sorted(comports()), 1):
            port_str = port_id + ' - ' + port_desc
            ports.append(port_str)

        features = {'Ports':ports}

        if self._last_error:
            features['ERROR'] = self._last_error
            self._last_error = None

        return features

# -----

    def variables(self, news:dict):
        self._process_outputs(news)

# -----

    def timer(self, prepare:bool):
        self._process_inputs()

#######

    def _is_variable_active(self, name):
        val = str(Variable.get(name))

        if self.param['TrigVals1'] and self.param['TrigVals1'].find(val) >= 0:
            return True

        return False

# =====

    def _get_val_obj(self, val):
        if val:
            ret = self.param['RespVal1']
        else:
            ret = self.param['RespVal0']
        try:
            return json.loads(ret)
        except:
            return ret

# =====

    def _process_inputs(self):
        if not self._ser:
            return

        try:
            name = self.param['RespVarDSR']
            if name:
                val = self._ser.dsr
                if val != self._last_dsr:
                    self._last_dsr = val
                    Variable.set(name, self._get_val_obj(val))

            name = self.param['RespVarCTS']
            if name:
                val = self._ser.cts
                if val != self._last_cts:
                    self._last_cts = val
                    Variable.set(name, self._get_val_obj(val))

            name = self.param['RespVarRI']
            if name:
                val = self._ser.ri
                if val != self._last_ri:
                    self._last_ri = val
                    Variable.set(name, self._get_val_obj(val))

            name = self.param['RespVarCD']
            if name:
                val = self._ser.cd
                if val != self._last_cd:
                    self._last_cd = val
                    Variable.set(name, self._get_val_obj(val))

            name = self.param['RespVarRXD']
            if name:
                val = self._ser.in_waiting > 0   # Hack: pull RXD pin to low get at least 1 char in buffer
                if val:
                    self._ser.reset_input_buffer()   # Hack: This leaves in_waiting to 1 if RXD pin is still low
                if val != self._last_rxd:
                    self._last_rxd = val
                    Variable.set(name, self._get_val_obj(val))
        except Exception() as e:
            self._last_error = str(e)
            pass

# =====

    def _process_outputs(self, news):
        if not self._ser:
            return

        try:
            name = self.param['TrigVarDTR']
            if name and name in news:
                val = self._is_variable_active(name)
                if val != self._last_dtr:
                    self._last_dtr = val
                    self._ser.dtr = val

            name = self.param['TrigVarRTS']
            if name and name in news:
                val = self._is_variable_active(name)
                if val != self._last_rts:
                    self._last_rts = val
                    self._ser.rts = val

            name = self.param['TrigVarTXD']
            if name and name in news:
                val = self._is_variable_active(name)
                if val != self._last_txd:
                    self._last_txd = val
                    self._ser.break_condition = val
        except Exception() as e:
            self._last_error = str(e)
            pass

# =====

    def _reset_state(self):
        self._last_dtr = None
        self._last_rts = None
        self._last_txd = None

        self._last_dsr = None
        self._last_cts = None
        self._last_ri  = None
        self._last_cd  = None
        self._last_rxd = None

#######
