"""
Machine Plugin for XXX
"""
import machine
import sys
if sys.platform != 'esp32':
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

MAPID = 'maESP32'
PTYPE = PT_MACHINE
PNAME = 'ESP32'
PINFO = '???'

LIST_PIN_IO = (
"36 (IN only)",
"39 (IN only)",
"34 (IN only)",
"35 (IN only)",
"32",
"33",
"25",
"26",
"27",
"14 (CLK)",
"12 (MISO)",
"13 (MOSI)",
"9 (RX1)",
"10 (TX1)",
"11",
"6",
"7",
"8",
"15 (SS)",
"2 (LED)",
"0 (Boot)",
"4",
"16 (RX2,no IRQ)",
"17 (TX2)",
"5 (vSS)",
"18 (vSCK)",
"19 (vMISO)",
"21 (SDA)",
"3 (RX0)",
"1 (TX0)",
"22 (SCL)",
"23 (vMOSI)",
)

LIST_I2C = (
"4,5 (WeMos LoLin32 +OLED)",
"15,4 (ESP32 +LoRa +OLED)",
"22,21 (BOB)",
)

LIST_SPI = (
"SPI (14,13,12,15)",
"SPI v (18,23,19,5)",
)

LIST_UART = (
"UART 0 (1,3)",
"UART 1 (10,9)",
"UART 2 (17,16)",
)

LIST_ADC = (
"CH0 (36)",
"CH1 (37)",
"CH2 (38)",
"CH3 (39)",
"CH4 (32)",
"CH5 (33)",
"CH6 (34)",
"CH7 (35)",
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
        Machine.set_feature('I2C', LIST_I2C)
        Machine.set_feature('SPI', LIST_SPI)
        Machine.set_feature('UART', LIST_UART)

        Machine.set_handler_class('PIN_IO', Pin_ESP32)
        Machine.set_handler_class('I2C', I2C_ESP32)
        Machine.set_handler_class('ADC', ADC_ESP32)

# -----

    def exit(self):
        super().exit()

#######

class Pin_ESP32(machine.Pin):
    def __init__(self, id, *args, **kwargs):
        if type(id) is str:
            id = int(id.strip().split(' ', 1)[0])
        super().__init__(id, *args, **kwargs)

    def set(self, v):
        self.value(v)

    def get(self):
        return self.value()

    val = property(get, set)

# =====

class I2C_ESP32(machine.I2C):
    def __init__(self, id='22,21'):
        if type(id) is str:
            id = id.strip().split(' ', 1)[0]
            sclid, sdaid = id.split(',', 2)
        elif type(id) is tuple:
            sclid, sdaid = id[:2]
        else:
            raise Exception('Wrong data type for id')
        self._scl_pin=machine.Pin(int(sclid))
        self._sda_pin=machine.Pin(int(sdaid))
        super().__init__(-1, self._scl_pin, self._sda_pin)

    def set_freq(self, freq=400000):
        self.init(self._scl_pin, self._sda_pin, freq=freq)

# =====

class ADC_ESP32():
    __adc = machine.ADC()

    def __init__(self, id):
        if type(id) is str:
            id = id.strip().split(' ', 1)[0]
            if id.startswith('CH'):
                id = id[2:]
        self._id = int(id)
        self._ch = self.__adc.channel(self._id)

    def read(self):
        return self._ch()

