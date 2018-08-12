"""
Machine Plugin for Testing on PC
"""
import pigpio

REMOTE_URL = '10.23.42.20'
PI = pigpio.pi(REMOTE_URL)

from com.Globals import *

import dev.Machine as Machine

#######
# Globals:

MAPID = 'maPCpigpio'
PTYPE = PT_MACHINE
PNAME = 'PCpigpio'


LIST_I2C = (
"I2C1 (GPIO03,GPIO02)",
)

#######

class PluginMachine(Machine.PluginMachineBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # instance specific params
            #'RemoteURL':'10.23.42.92',
            }

# -----

    def init(self):
        super().init()

        #self._pi = pigpio.pi(self.param['RemoteURL'])
        #I2C_PC._pi = self._pi

        Machine.set_feature('I2C', LIST_I2C)

        Machine.set_handler_class('I2C', I2C_PC)

# -----

    def exit(self):
        super().exit()

#######

class I2C_PC():
    _pi = PI

    def __init__(self, id='1'):
        if type(id) is str:
            id = id.strip().split(' ', 1)[0]
            if id.startswith('I2C'):
                id = id[3:]
            self._id = int(id)
        elif type(id) is int:
            self._id = id
        else:
            raise Exception('Wrong data type for id')
        #self._pi = pigpio.pi(REMOTE_URL)
        self._h = None

    def init(self, addr, freq=400000):
        if type(addr) is str:
            addr = addr.strip().split(' ', 1)[0]
            self._addr = int(addr, 0)
        elif type(addr) is int:
            self._addr = addr
        else:
            raise Exception('Wrong data type for addr')
        if not 0 <= self._addr <= 127:
            raise Exception('Wrong addr - out of range')
        self._h = self._pi.i2c_open(self._id, self._addr)

    def deinit(self):
        self._pi.i2c_close(self._h)
    
    def set_freq(self, freq=400000):
        #self.init(self._scl_pin, self._sda_pin, freq=freq)
        pass


    def read_byte(self) -> int:
        return self._pi.i2c_read_byte(self._h)

    def write_byte(self, data:int):
        self._pi.i2c_write_byte(self._h, data)

    def read_reg_byte(self, reg:int) -> int:
        return self._pi.i2c_read_byte_data(self._h, reg)

    def write_reg_byte(self, reg:int, data:int):
        self._pi.i2c_write_byte_data(self._h, reg, data)

    def read_reg_word(self, reg:int, little_endian=True, signed=False) -> int:
        data =  self._pi.i2c_read_word_data(self._h, reg)
        if not little_endian:
            data = ((data & 0xFF) << 8) | ((data & 0xFF00) >> 8)
        if signed and (data >= 32768):
            data -= 65536
        return data        

    def write_reg_word(self, reg:int, data:int, little_endian=True):
        if not little_endian:
            data = ((data & 0xFF) << 8) | ((data & 0xFF00) >> 8)
        self._pi.i2c_write_word_data(self._h, reg, data)

    def read_reg_buffer(self, reg:int, nbytes:int) -> bytearray:
        return self._pi.i2c_read_i2c_block_data(self._h, reg, nbytes)

    def write_reg_buffer(self, reg:int, data:bytearray):
        self._pi.i2c_write_i2c_block_data(self._h, reg, data)

    def read_buffer(self, nbytes:int) -> bytearray:
        return self._pi.i2c_read_device(self._h, nbytes)[1]

    def write_buffer(self, data:bytearray):
        self._pi.i2c_write_device(self._h, data)

# =====


