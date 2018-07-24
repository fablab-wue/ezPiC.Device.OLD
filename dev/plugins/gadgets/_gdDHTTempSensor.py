"""
Temperature Sensors supported by the "dht" micropython module
MicroPython ONLY!
"""
from com.Globals import *

if not MICROPYTHON:
    raise Exception('module not designed for CPython')

import machine
import dht

import com.Tool as Tool
import dev.Gadget as Gadget

#######
# Globals:

EZPID = 'gdDHTTempHumSensorGadget'
PTYPE = PT_SENSOR
PNAME = 'DHT / AM Temperature and Humidity Sensor Gadget'

#######


class PluginGadget(Gadget.PluginGadgetBase):

    def __init__(self, module): # FIXME in base class, everywhere: shadowing of "module"
        super().__init__(module)
        self.param = {
            'NAME': 'DHT / AM Temperature and Humidity Sensor Gadget', 
            'machine_pin': 4, 
            'type': 'DHT11'
            } # TODO Allowed values / Lists / ...?
        self.timer_period = 3 # must be at least 1 (DHT11 type) or 2 (DHT22 type)
        self._sensor = None # TODO There should be a better way. (Gadget.setup(..) or whatever)

# -----

    def timer(self, prepare:bool):
        if self._sensor is None:
            if self.param['type'] == "DHT11":
                # TODO try: Error reporting?
                self._sensor = dht.DHT11(machine.Pin(self.param['machine_pin']))
            elif self.param['type'] == "DHT22":
                self._sensor = dht.DHT22(machine.Pin(self.param['machine_pin']))

        self._sensor.measure()
        temp = self._sensor.temperature()
        hum = self._sensor.humidity()
        # TODO Where to go from here?

#######
