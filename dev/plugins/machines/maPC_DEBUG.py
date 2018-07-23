"""
Machine Plugin for Testing on PC
"""
import sys
if sys.platform != 'win32':
    raise Exception

from com.Globals import *

import dev.Machine as Machine

#######
# Globals:

MAPID = 'maPCDEBUG'
PTYPE = PT_MACHINE
PNAME = 'PC DEBUG'
PINFO = '???'

LIST_PIN_IO = (   # TEST ONLY
"GPIO0 (Lorem)",
"GPIO1 (Ipsum)",
"GPIO2 (Dolor)",
"GPIO3 (Sit)",
"GPIO4 (Amet)",
)

LIST_SPI = (
"SPI0 (GPIO11,GPIO10,GPIO09,GPIO08/07)",
"SPI1 (GPIO21,GPIO20,GPIO19)",
)

LIST_I2C = (
"I2C1 (Lorem)",
"I2C2 (Ipsum)",
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

        Machine.set_handler_class('PIN_IO', Pin_PC)
        Machine.set_handler_class('I2C', I2C_PC)

# -----

    def exit(self):
        super().exit()

#######

class Pin_PC():
    IN =            1
    OUT =           2
    OPEN_DRAIN =    3
    PULL_UP =       4
    PULL_DOWN =     5

    def __init__(self, id:str, mode=-1):
        id = str(id).strip().split(' ', 1)[0]
        if id.startswith('GPIO'):
            id = id[4:]
        self._id = int(id)
        self._val = 0
        print('PinPC __init__', id)

    
    def init(self, mode=-1, pull=-1, *, value):
        print('PinPC init', mode, pull)

    def mode(self, m):
        print('PinPC mode', m)

    def set(self, v):
        self._val = v
        print('PinPC set', v)

    def get(self):
        print('PinPC get')
        return self._val

    def value(self, v=None):
        if v:
            self.set(v)
        else:
            return self.get()

    def __call__(self, v=None):
        if v:
            self.set(v)
        else:
            return self.get()

    val = property(get, set)

# =====

class I2C_PC():
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
        self._i2c = self._id

    def init(self, scl, sda, *, freq=400000):
        pass

    def deinit(self):
        pass
    
    def readfrom(self, addr, nbytes, stop=True):
        print('I2C.readfrom {} {}'.format(addr, nbytes))
        buf = bytearray(nbytes)
        return buf

    def readfrom_into(self, addr, buf, stop=True):
        print('I2C.readfrom_into {} {}'.format(addr, buf))
        for i in range(len(buf)):
            buf[i] = i

    def writeto(self, addr, buf, stop=True):
        print('I2C.writeto {} {}'.format(addr, buf))

    def readfrom_mem(self, addr, memaddr, nbytes, *, addrsize=8):
        print('I2C.readfrom_mem {} {} {}'.format(addr, memaddr, nbytes))
        return [0]

    def readfrom_mem_into(self, addr, memaddr, buf, *, addrsize=8):
        print('I2C.readfrom_mem_into {} {} {}'.format(addr, memaddr, buf))

    def writeto_mem(self, addr, memaddr, buf, *, addrsize=8):
        print('I2C.writeto_mem {} {} {}'.format(addr, memaddr, buf))
        self._i2c.write_i2c_block_data(addr, memaddr, buf)
    
    def set_freq(self, freq=400000):
        print('I2C.set_freq {}'.format(freq))
        #self.init(self._scl_pin, self._sda_pin, freq=freq)

    def testwrite(self, addr, reg, data):
        self._i2c.write_byte_data(addr, reg, data)


        data = self._i2c.read_byte_data(addr, reg)

# =====

