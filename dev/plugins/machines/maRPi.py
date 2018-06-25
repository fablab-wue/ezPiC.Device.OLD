"""
Machine Plugin for Raspberry Pi
"""
import RPi.GPIO as GPIO

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

MAPID = 'maRPi'
PTYPE = PT_MACHINE
PNAME = 'Raspberry Pi'
PINFO = '???'

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
"I2C0 (GPIO01,GPIO00) DNC",
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

        Machine.set_handler_class('PIN_IO', Pin_RPi)

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

