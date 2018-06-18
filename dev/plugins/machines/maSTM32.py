"""
Machine Plugin for XXX
"""
import machine
import sys
if sys.platform != 'pyboard':
    raise

from com.Globals import *

import dev.Machine as Machine

# PyBoard
#p = Pin_RPi('A8', 1)
#c = Pin_RPi
#pp = c('A10', 1)

#ESP32
#p = Pin_RPi(2, 1)

#LoPy
#p = Pin_RPi('P9', 2)

#######
# Globals:

MAPID = 'PYB'
PNAME = 'PyBoard'
PINFO = '???'

LIST_PIN_IO = (
"A0 (X1)",
"A1 (X2)",
"A2 (X3)",
"A3 (X4)",
"A4 (X5)",
"A5 (X6)",
"A6 (X7)",
"A7 (X8)",
"A8",
"A10",
"A13 (P5)",
"A14 (P4)",
"A15 (P3)",
"B0 (Y11)",
"B1 (Y12)",
"B2",
"B3 (X17)",
"B4 (P2)",
"B6 (X9)",
"B7 (X10)",
"B8 (Y3)",
"B9 (Y4)",
"B10 (Y9)",
"B11 (Y10)",
"B12 (Y5)",
"B13 (Y6)",
"B14 (Y7)",
"B15 (Y8)",
"C0 (X19)",
"C1 (X20)",
"C2 (X21)",
"C3 (X22)",
"C4 (X11)",
"C5 (X12)",
"C6 (Y1)",
"C7 (Y2)",
"C13 (X18)",
)

LIST_PIN_ADC = (
"A0 (X1)",
"A1 (X2)",
"A2 (X3)",
"A3 (X4)",
"A4 (X5)",
"A5 (X6)",
"A6 (X7)",
"A7 (X8)",
"B0 (Y11)",
"B1 (Y12)",
"C0 (X19)",
"C1 (X20)",
"C2 (X21)",
"C3 (X22)",
"C4 (X11)",
"C5 (X12)",
)

LIST_PIN_DAC = (
"A4 (X5)",
"A5 (X6)",
)

LIST_I2C = (
"I2C 1 (B6,B7)",
"I2C 2 (B10,B11)",
)

LIST_SPI = (
"SPI 1 (A5,A6,A7,A4)",
"SPI 2 (B13,B14,B15,B12)",
)

LIST_UART = (
"UART 1 (B6,B7)",
"UART 2 (A2,A3)",
"UART 3 (B10,B11)",
"UART 4 (A0,A1)",
"UART 6 (C6,C7)",
)

LIST_CAN = (
"CAN 1 (B9,B8)",
"CAN 2 (B13,B12)",
)


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
        Machine.set_feature('PIN_IO', LIST_PIN_IO)
        Machine.set_feature('PIN_I', LIST_PIN_IO)
        Machine.set_feature('PIN_O', LIST_PIN_IO)
        Machine.set_feature('PIN_ADC', LIST_PIN_ADC)
        Machine.set_feature('PIN_DAC', LIST_PIN_DAC)
        Machine.set_feature('I2C', LIST_I2C)
        Machine.set_feature('SPI', LIST_SPI)
        Machine.set_feature('UART', LIST_UART)
        Machine.set_feature('CAN', LIST_CAN)

        Machine.set_handler_class('PIN_IO', Pin_PyB)

# -----

    def exit(self):
        super().exit()

#######

class Pin_PyB(machine.Pin):
    def __init__(self, id, *args, **kwargs):
        id = id.strip().split(' ', 1)[0]
        super().__init__(id, *args, **kwargs)

    def set(self, v):
        self.value(v)

    def get(self):
        return self.value()

    val = property(get, set)


