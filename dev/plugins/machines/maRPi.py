"""
Machine Plugin for Raspberry Pi
"""
import RPi.GPIO as GPIO
import smbus
import serial
from serial.tools.list_ports import comports

from com.Globals import *

import dev.Machine as Machine

#######
# Globals:

MAPID = 'maRPi'
PTYPE = PT_MACHINE
PNAME = 'Raspberry Pi'

LIST_PIN_IO = (
"GPIO00 (Pin3@Rev1)",
"GPIO01 (Pin5@Rev1)",
"GPIO02 (Pin3@Rev2,SDA)",
"GPIO03 (Pin5@Rev2,SCL)",
"GPIO04 (Pin7)",
"GPIO05 (Pin29)",
"GPIO06 (Pin31)",
"GPIO07 (Pin26,CE1)",
"GPIO08 (Pin24,CE0)",
"GPIO09 (Pin21,MISO)",
"GPIO10 (Pin19,MOSI)",
"GPIO11 (Pin23,CLK)",
"GPIO12 (Pin32,PWM0)",
"GPIO13 (Pin33,PWM1)",
"GPIO14 (Pin8,TX)",
"GPIO15 (Pin10,RX)",
"GPIO16 (Pin36)",
"GPIO17 (Pin11)",
"GPIO18 (Pin12,PWM0)",
"GPIO19 (Pin35)",
"GPIO20 (Pin38)",
"GPIO21 (Pin40)",
"GPIO22 (Pin15)",
"GPIO23 (Pin16)",
"GPIO24 (Pin18)",
"GPIO25 (Pin22)",
"GPIO26 (Pin37)",
"GPIO27 (Pin13)",
)

LIST_SPI = (
"SPI0 (GPIO11,GPIO10,GPIO09,GPIO08/07)",
"SPI1 (GPIO21,GPIO20,GPIO19)",
)

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
            'abc':123,
            'xyz':456,
            }

# -----

    def init(self):
        super().init()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        Machine.set_feature('PIN_IO', LIST_PIN_IO)
        Machine.set_feature('PIN_I', LIST_PIN_IO)
        Machine.set_feature('PIN_O', LIST_PIN_IO)
        Machine.set_feature('I2C', LIST_I2C)
        Machine.set_feature('SPI', LIST_SPI)

        ports = []
        for n, (port_id, port_desc, hwid) in enumerate(sorted(comports()), 1):
            port_str = port_id + ' - ' + port_desc
            ports.append(port_str)
        Machine.set_feature('UART', ports)
        print(ports)

        Machine.set_handler_class('PIN_IO', Pin_RPi)
        Machine.set_handler_class('UART', UART_RPi)
        Machine.set_handler_class('I2C', I2C_RPi)

# -----

    def exit(self):
        super().exit()

#######

class Pin_RPi():
    IN =            GPIO.IN
    OUT =           GPIO.OUT
    OPEN_DRAIN =    GPIO.OUT
    PULL_UP =       GPIO.PUD_UP
    PULL_DOWN =     GPIO.PUD_DOWN

    def __init__(self, id:str, mode=IN):
        id = id.strip().split(' ', 1)[0]
        if id.startswith('GPIO'):
            id = id[4:]
        self._id = int(id)
    
    def init(self, mode=-1, pull=-1, *, value):
        GPIO.setup(self._id, mode)
        #GPIO.setup(port_or_pin, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN) # input with pull-down  
        #GPIO.setup(port_or_pin, GPIO.IN,  pull_up_down=GPIO.PUD_UP)   # input with pull-up   
        #GPIO.setup(port_or_pin, GPIO.OUT, initial=1)    # set initial value option (1 or 0)  

    def mode(self, mode):
        GPIO.setup(self._id, mode)

    def set(self, v):
        GPIO.output(self._id, v)

    def get(self):
        return GPIO.input(self._id)

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

#GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback)
#def my_callback(channel): 
#GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=200)
#GPIO.remove_event_detect(port_number)
#GPIO.add_event_detect(25, GPIO.BOTH, callback=my_callback)

'''
GPIO.setup(25, GPIO.OUT)# set GPIO 25 as an output. You can use any GPIO port  
  
p = GPIO.PWM(25, 50)    # create an object p for PWM on port 25 at 50 Hertz  
                        # you can have more than one of these, but they need  
                        # different names for each port   
                        # e.g. p1, p2, motor, servo1 etc.  
  
p.start(50)             # start the PWM on 50 percent duty cycle  
                        # duty cycle value can be 0.0 to 100.0%, floats are OK  
  
p.ChangeDutyCycle(90)   # change the duty cycle to 90%  
  
p.ChangeFrequency(100)  # change the frequency to 100 Hz (floats also work)  
                        # e.g. 100.5, 5.2  
  
p.stop()                # stop the PWM output  
'''

# =====

class UART_RPi():
    def __init__(self, id='/dev/ttyAMA0'):
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

class I2C_RPi():
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
        self._i2c = smbus.SMBus(self._id)

    def init(self, scl, sda, *, freq=400000):
        pass

    def deinit(self):
        pass
    
    def readfrom(self, addr, nbytes, stop=True):
        buf = bytearray(nbytes)
        self.readfrom_into(addr, buf, stop)
        return buf

    def readfrom_into(self, addr, buf, stop=True):
        for i in range(len(buf)):
            data = self._i2c.read_byte(addr)
            buf[i] = data

    def writeto(self, addr, buf, stop=True):
        for i in range(len(buf)):
            self._i2c.write_byte(addr, buf[i])

    def readfrom_mem(self, addr, memaddr, nbytes, *, addrsize=8):
        buf = self._i2c.read_i2c_block_data(addr, memaddr)
        return buf

    def readfrom_mem_into(self, addr, memaddr, buf, *, addrsize=8):
        buf = self._i2c.read_i2c_block_data(addr, memaddr)

    def writeto_mem(self, addr, memaddr, buf, *, addrsize=8):
        self._i2c.write_i2c_block_data(addr, memaddr, buf)
    
    def set_freq(self, freq=400000):
        #self.init(self._scl_pin, self._sda_pin, freq=freq)
        pass

    def testwrite(self, addr, reg, data):
        self._i2c.write_byte_data(addr, reg, data)


        data = self._i2c.read_byte_data(addr, reg)


# =====

