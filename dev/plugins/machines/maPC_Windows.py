"""
Machine Plugin for Testing on PC
"""
import sys
if sys.platform != 'win32':
    raise Exception

import serial
from serial.tools.list_ports import comports

from com.Globals import *

import dev.Machine as Machine

#######
# Globals:

MAPID = 'maPC'
PTYPE = PT_MACHINE
PNAME = 'PC'

#######

class PluginMachine(Machine.PluginMachineBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # instance specific params
            'abc':123,
            'xyz':456,
            }

# -----

    def init(self):
        super().init()
        ports = []
        for n, (port_id, port_desc, hwid) in enumerate(sorted(comports()), 1):
            port_str = port_id + ' - ' + port_desc
            ports.append(port_str)
        Machine.set_feature('UART', ports)

        Machine.set_handler_class('UART', UART_PC)

# -----

    def exit(self):
        super().exit()

#######

class UART_PC():
    def __init__(self, id='COM1'):
        if type(id) is str:
            id = id.strip().split(' ', 1)[0]
        self._ser = serial.Serial()
        self._ser.port = id

    def __del__(self):
        self._ser.close()

    def init(self, baudrate, bits=8, parity=None, stop=1):
        if not self._ser:
            return
        if self._ser.is_open:
            self._ser.close()

        self._ser.baudrate = baudrate
        self._ser.bits = bits
        self._ser.bytesize = bits
        self._ser.stopbits = stop
        if parity == 0:
            self._ser.parity = 'E'
        elif parity == 1:
            self._ser.parity = 'O'
        else:
            self._ser.parity = 'N'

        self._ser.open()

    def deinit(self):
        if self._ser:
            self._ser.close()
            self._ser = None

    def any(self):
        if not self._ser:
            return 0
        return self._ser.in_waiting

    def read(self, nbytes=1):
        if not self._ser:
            return None
        return self._ser.read(nbytes)

    def write(self, buf):
        if not self._ser:
            return 0
        return self._ser.write(buf)

    def sendbreak(self):
        if not self._ser:
            return
        self._ser.send_break(0.0001)

    def set_dtr(self, dtr):
        if not self._ser:
            return
        self._ser.dtr = dtr

    def set_rts(self, rts):
        if not self._ser:
            return
        self._ser.rts = rts

# =====


