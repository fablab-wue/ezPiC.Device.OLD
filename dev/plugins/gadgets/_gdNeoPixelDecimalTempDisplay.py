"""
A demo device for a room thermometer in pseudonixie style as described ...
MicroPython ONLY!
"""
# TODO Make one and publish design files for it..
from com.Globals import *

if not MICROPYTHON:
    raise Exception('module not designed for CPython')

import machine
import neopixel

import com.Tool as Tool
import dev.Gadget as Gadget

#######
# Globals:

GDPID = 'NeoPixelDecimalTempDisplayGadget'
PNAME = 'NeoPixel Decimal Temperature Display'
PINFO = 'Display a (room) temperature measurement as a decimal coded value on a NeoPixel controlled LED strip with a temperature related colour gradient.'

#######

COLOUR_40 = (255,40,40)
COLOUR_1 = (255,200,40)
COLOUR_0 = (40,200,255)
COLOUR_n20 = (40,20,255)


class PluginGadget(Gadget.PluginGadgetBase):
    def __init__(self, module): # FIXME in base class, everywhere: shadowing of "module"
        super().__init__(module)
        self.param = {
            'NAME': 'NeoPixel Decimal Display', 
            'machine_pin': 3, 
            'int_digits': 2, 
            'fract_digits': 1,
            'measurement': ['temp'],
            }
        self.timer_period = 12

        self._num_leds = (self.param['int_digits' + self.param['fract_digits']]) * 10
        self._np = neopixel.NeoPixel(machine.Pin(self.param['machine_pin']), self._num_leds)

# -----

    def output_value(self, value):
        colour = (0, 0, 0)
        if value <= 0:
            # lerp with tuples: colour = COLOUR_0 + ( (COLOUR_n20 - COLOUR_0) * (min(abs(value), 20) / 20) )
            colour = tuple(a - b for a, b in zip(COLOUR_n20, COLOUR_0))
            colour = tuple(a + (b * (min(abs(value), 20) / 20)) for a, b in zip(COLOUR_0, colour))
        if value > 0:
            # lerp with tuples: colour = COLOUR_1 + (COLOUR_40 - COLOUR_1) * (min(value, 40) / 40)
            colour = tuple(a - b for a, b in zip(COLOUR_40, COLOUR_1))
            colour = tuple(a + (b * (min(abs(value), 20) / 20)) for a, b in zip(COLOUR_1, colour))
        string_value = ''
        if self.param['fract_digits'] > 0:
            string_value = '{:' + (self.param['int_digits'] + self.param['fract_digits'] + 1) +\
                           '.' + self.param['fract_digits'] + 'f}'.format(abs(value))
            string_value = string_value.replace('.', '')
        else:
            string_value = '{:' + self.param['int_digits'] + '.0f}'.format(abs(value))
        for c_index in range(len(string_value)):
            for n in range(10):
                v = ord(string_value[c_index]) - ord('0')
                if v == n:
                    self._np[(c_index * 10) + n] = colour
                else:
                    self._np[(c_index * 10) + n] = (0,0,0)
        self._np.write()

# -----

    def output_error(self, error_number):
        for c_index in range(self._num_leds / 10):
            for n in range(10):
                if error_number == n:
                    self._np[(c_index * 10) + n] = (255,0,255)
                else:
                    self._np[(c_index * 10) + n] = (0,0,0)
        self._np.write()

# -----

    def timer(self, prepare:bool):
        # TODO Ja doof, gibt noch gar keine Werteverwaltung.
        display_temp = gib_das_measurement(self.param['measurement'])
        if display_temp is None:
            self.output_error(0)
        else:
            self.output_value(display_temp)

#######
