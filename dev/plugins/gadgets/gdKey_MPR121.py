"""
Gadget Plugin for Touch Key MPR121
based on https://github.com/adafruit/Adafruit_Python_MPR121
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdMPR121'
PTYPE = PT_SENSOR
PNAME = '@PLAN Key - MPR121 - 12-Ch Touch Key Pad (I2C)'

MPR121_I2CADDR_DEFAULT = 0x5A
MPR121_TOUCHSTATUS_L   = 0x00
MPR121_TOUCHSTATUS_H   = 0x01
MPR121_FILTDATA_0L     = 0x04
MPR121_FILTDATA_0H     = 0x05
MPR121_BASELINE_0      = 0x1E
MPR121_MHDR            = 0x2B
MPR121_NHDR            = 0x2C
MPR121_NCLR            = 0x2D
MPR121_FDLR            = 0x2E
MPR121_MHDF            = 0x2F
MPR121_NHDF            = 0x30
MPR121_NCLF            = 0x31
MPR121_FDLF            = 0x32
MPR121_NHDT            = 0x33
MPR121_NCLT            = 0x34
MPR121_FDLT            = 0x35
MPR121_TOUCHTH_0       = 0x41
MPR121_RELEASETH_0     = 0x42
MPR121_DEBOUNCE        = 0x5B
MPR121_CONFIG1         = 0x5C
MPR121_CONFIG2         = 0x5D
MPR121_CHARGECURR_0    = 0x5F
MPR121_CHARGETIME_1    = 0x6C
MPR121_ECR             = 0x5E
MPR121_AUTOCONFIG0     = 0x7B
MPR121_AUTOCONFIG1     = 0x7C
MPR121_UPLIMIT         = 0x7D
MPR121_LOWLIMIT        = 0x7E
MPR121_TARGETLIMIT     = 0x7F
MPR121_GPIODIR         = 0x76
MPR121_GPIOEN          = 0x77
MPR121_GPIOSET         = 0x78
MPR121_GPIOCLR         = 0x79
MPR121_GPIOTOGGLE      = 0x7A
MPR121_SOFTRESET       = 0x80

INIT_SEQUENCE = (
    (MPR121_ECR, 0x00),
    (MPR121_MHDR, 0x01),
    (MPR121_NHDR, 0x01),
    (MPR121_NCLR, 0x0E),
    (MPR121_FDLR, 0x00),
    (MPR121_MHDF, 0x01),
    (MPR121_NHDF, 0x05),
    (MPR121_NCLF, 0x01),
    (MPR121_FDLF, 0x00),
    (MPR121_NHDT, 0x00),
    (MPR121_NCLT, 0x00),
    (MPR121_FDLT, 0x00),
    (MPR121_DEBOUNCE, 0),
    (MPR121_CONFIG1, 0x10), # default, 16uA charge current
    (MPR121_CONFIG2, 0x20), # 0.5uS encoding, 1ms period
    (MPR121_ECR, 0x8F),  # start with first 5 bits of baseline tracking
    )

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'MPR121',
            'ENABLE':False,
            'TIMER':2.1,
            'PORT':'1',
            'ADDR':'5B',
            # instance specific params
            'RespVarKey':'ScanKey',
            'RespVarCode':'MPR121.ScanCode',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        self._i2c.write_reg_byte(MPR121_SOFTRESET, 0x63)

        for reg, val in INIT_SEQUENCE:
            self._i2c.write_reg_byte(reg, val)

        self.set_thresholds(12, 6)

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('5A (ADDR-VDD)', '5B (ADDR-GND)', '5C (ADDR-SDA)', '5D (ADDR-SCL)')

# -----

    def timer(self, prepare:bool):
        name = self.param['RespVarCode']
        if name:
            val = touched()
            print(val)
            if val != self._last_val:
                self._last_val = val
                Variable.set(name, val)

# =====

    def set_thresholds(self, touch, release):
        """Set the touch and release threshold for all inputs to the provided
        values.  Both touch and release should be a value between 0 to 255
        (inclusive).
        """
        assert touch >= 0 and touch <= 255, 'touch must be between 0-255 (inclusive)'
        assert release >= 0 and release <= 255, 'release must be between 0-255 (inclusive)'
        # Set the touch and release register value for all the inputs.
        for i in range(12):
            self._i2c.write_reg_byte(MPR121_TOUCHTH_0 + 2*i, touch)
            self._i2c.write_reg_byte(MPR121_RELEASETH_0 + 2*i, release)

    def filtered_data(self, pin):
        """Return filtered data register value for the provided pin (0-11).
        Useful for debugging.
        """
        assert pin >= 0 and pin < 12, 'pin must be between 0-11 (inclusive)'
        return self._i2c.read_reg_word(MPR121_FILTDATA_0L + pin*2)

    def baseline_data(self, pin):
        """Return baseline data register value for the provided pin (0-11).
        Useful for debugging.
        """
        assert pin >= 0 and pin < 12, 'pin must be between 0-11 (inclusive)'
        bl = self._i2c.read_reg_byte(MPR121_BASELINE_0 + pin)
        return bl << 2

    def touched(self):
        """Return touch state of all pins as a 12-bit value where each bit 
        represents a pin, with a value of 1 being touched and 0 not being touched.
        """
        t = self._i2c.read_reg_word(MPR121_TOUCHSTATUS_L)
        return t & 0x0FFF

    def is_touched(self, pin):
        """Return True if the specified pin is being touched, otherwise returns
        False.
        """
        assert pin >= 0 and pin < 12, 'pin must be between 0-11 (inclusive)'
        t = self.touched()
        return (t & (1 << pin)) > 0

#######
