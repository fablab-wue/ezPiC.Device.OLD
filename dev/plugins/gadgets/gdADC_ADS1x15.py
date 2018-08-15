"""
Gadget Plugin for ADC ADS1x15
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdADS1x15'
PTYPE = PT_SENSOR
PNAME = '@TEST ADC - ADS1015, ADS1115 - 4-Ch 12/16-Bit ADC (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'ADS1x15',
            'ENABLE':False,
            'TIMER':5,
            'PORT':'1',
            'ADDR':'48',
            # instance specific params
            'RespVar':'ADS1x15.value',
            'PGA':'1',
            'Mux':'4',
            'MapADC0':0,
            'MapADC1':0,
            'MapVal0':'0.0',
            'MapVal1':'100.0',
            }

# -----

    def init(self):
        super().init()

        #test = self._i2c.read_reg_word(1, little_endian=False) # MSB first

        mux = 0x4
        pga = 0x1
        sps = 0x0
        if self._i2c and self.param['Mux']:
            mux = int(self.param['Mux'], 0)
        if self._i2c and self.param['PGA']:
            pga = int(self.param['PGA'], 0)
 
        data = (1 << 15) | (mux << 12) | (pga << 9) | (sps << 5)
        self._i2c.write_reg_word(1, data, little_endian=False)

        self._map_adc_0 = 0
        self._map_adc_1 = 0
        self._map_val_0 = 0
        self._map_val_1 = 0
        if self._i2c and self.param['MapADC0']:
            self._map_adc_0 = int(self.param['MapADC0'])
        if self._i2c and self.param['MapADC1']:
            self._map_adc_1 = int(self.param['MapADC1'])
        if self._i2c and self.param['MapVal0']:
            self._map_val_0 = float(self.param['MapVal0'])
        if self._i2c and self.param['MapVal1']:
            self._map_val_1 = float(self.param['MapVal1'])

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('48 (ADDR-GND)', '49 (ADDR-VDD)', '4A (ADDR-SDA)', '4B (ADDR-SCL)')

# -----

    def timer(self, prepare:bool):
        name = self.param['RespVar']
        if name:
            val = self._i2c.read_reg_word(0, little_endian=False, signed=True)
            #print(val)
            if self._map_adc_0 != self._map_adc_1:
                val = (val - self._map_adc_0) \
                    / (self._map_adc_1 - self._map_adc_0) \
                    * (self._map_val_1 - self._map_val_0) \
                    + self._map_val_0
                #print(val)
            Variable.set(name, val)

#######
