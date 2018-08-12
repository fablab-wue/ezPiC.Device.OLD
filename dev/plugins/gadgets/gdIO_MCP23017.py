"""
Gadget Plugin for IO MCP23017
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdMCP23017'
PTYPE = PT_SENSOR | PT_ACTUATOR
PNAME = '@WORK IO - MCP23017 - 16-Bit Port Expander (I2C)'

MCP23017_IODIRA	 =	0x00 # I/O DIRECTION REGISTER   IO7 IO6 IO5 IO4 IO3 IO2 IO1 IO0 1111 1111
MCP23017_IODIRB	 =	0x01 # I/O DIRECTION REGISTER   IO7 IO6 IO5 IO4 IO3 IO2 IO1 IO0 1111 1111
MCP23017_IPOLA	 =  0x02 # INPUT POLARITY PORT REGISTER   IP7 IP6 IP5 IP4 IP3 IP2 IP1 IP0 0000 0000
MCP23017_IPOLB	 =  0x03 # INPUT POLARITY PORT REGISTER   IP7 IP6 IP5 IP4 IP3 IP2 IP1 IP0 0000 0000
MCP23017_GPINTENA=  0x04 # INTERRUPT-ON-CHANGE PINS   GPINT7 GPINT6 GPINT5 GPINT4 GPINT3 GPINT2 GPINT1 GPINT0 0000 0000
MCP23017_GPINTENB=	0x05 # INTERRUPT-ON-CHANGE PINS   GPINT7 GPINT6 GPINT5 GPINT4 GPINT3 GPINT2 GPINT1 GPINT0 0000 0000
MCP23017_DEFVALA =	0x06 # DEFAULT VALUE REGISTER   DEF7 DEF6 DEF5 DEF4 DEF3 DEF2 DEF1 DEF0 0000 0000
MCP23017_DEFVALB =	0x07 # DEFAULT VALUE REGISTER   DEF7 DEF6 DEF5 DEF4 DEF3 DEF2 DEF1 DEF0 0000 0000
MCP23017_INTCONA =	0x08 # INTERRUPT-ON-CHANGE CONTROL REGISTER   IOC7 IOC6 IOC5 IOC4 IOC3 IOC2 IOC1 IOC0 0000 0000
MCP23017_INTCONB =	0x09 # INTERRUPT-ON-CHANGE CONTROL REGISTER   IOC7 IOC6 IOC5 IOC4 IOC3 IOC2 IOC1 IOC0 0000 0000
MCP23017_IOCON	 =  0x0A # I/O EXPANDER CONFIGURATION REGISTER   BANK MIRROR SEQOP DISSLW HAEN ODR INTPOL — 0000 0000 - also on addr 0x0B
MCP23017_GPPUA	 =  0x0C # GPIO PULL-UP RESISTOR REGISTER   PU7 PU6 PU5 PU4 PU3 PU2 PU1 PU0 0000 0000
MCP23017_GPPUB	 =  0x0D # GPIO PULL-UP RESISTOR REGISTER   PU7 PU6 PU5 PU4 PU3 PU2 PU1 PU0 0000 0000
MCP23017_INTFA	 =  0x0E # INTERRUPT FLAG REGISTER   INT7 INT6 INT5 INT4 INT3 INT2 INT1 INTO 0000 0000
MCP23017_INTFB	 =  0x0F # INTERRUPT FLAG REGISTER   INT7 INT6 INT5 INT4 INT3 INT2 INT1 INTO 0000 0000
MCP23017_INTCAPA =	0x10 # INTERRUPT CAPTURED VALUE FOR PORT REGISTER   ICP7 ICP6 ICP5 ICP4 ICP3 ICP2 ICP1 ICP0 0000 0000
MCP23017_INTCAPB =	0x11 # INTERRUPT CAPTURED VALUE FOR PORT REGISTER   ICP7 ICP6 ICP5 ICP4 ICP3 ICP2 ICP1 ICP0 0000 0000
MCP23017_GPIOA	 =  0x12 # GENERAL PURPOSE I/O PORT REGISTER   GP7 GP6 GP5 GP4 GP3 GP2 GP1 GP0 0000 0000
MCP23017_GPIOB	 =  0x13 # GENERAL PURPOSE I/O PORT REGISTER   GP7 GP6 GP5 GP4 GP3 GP2 GP1 GP0 0000 0000
MCP23017_OLATA	 =  0x14 # OUTPUT LATCH REGISTER   OL7 OL6 OL5 OL4 OL3 OL2 OL1 OL0 0000 0000
MCP23017_OLATB	 =  0x15 # OUTPUT LATCH REGISTER   OL7 OL6 OL5 OL4 OL3 OL2 OL1 OL0 0000 0000

INIT_SEQUENCE = (
    (MCP23017_IODIRA,   0xFF),  # port A to input
    (MCP23017_GPPUA,    0xFF),  # port A pullup on
    (MCP23017_IODIRB,   0xFF),  # port B to input
    (MCP23017_GPPUB,    0xFF),  # port B pullup on
)

#######

class PluginGadget(GI2C):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'MCP23017',
            'ENABLE':False,
            'TIMER':3.1,
            'PORT':'1',
            'ADDR':'20',
            # instance specific params
            'InputA':'0xFF',
            'InitValA':'0x00',
            'TrigVarA':'MCP23017.A.out',
            'RespVarA':'MCP23017.A.in',
            'InputB':'0xFF',
            'InitValB':'0x00',
            'TrigVarB':'MCP23017.B.out',
            'RespVarB':'MCP23017.B.in',
            }
        self._last_val = None

# -----

    def init(self):
        super().init()

        for reg, val in INIT_SEQUENCE:
            self._i2c.write_reg_byte(reg, val)

        if self._i2c and self.param['InputA']:
            self._i2c.write_reg_byte(MCP23017_IODIRA, int(self.param['InputA'], 0))
            self._i2c.write_reg_byte(MCP23017_GPPUA, int(self.param['InputA'], 0))
        if self._i2c and self.param['InitValA']:
            self._i2c.write_reg_byte(MCP23017_GPIOA, int(self.param['InitValA'], 0))

        if self._i2c and self.param['InputB']:
            self._i2c.write_reg_byte(MCP23017_IODIRB, int(self.param['InputB'], 0))
            self._i2c.write_reg_byte(MCP23017_GPPUB, int(self.param['InputB'], 0))
        if self._i2c and self.param['InitValB']:
            self._i2c.write_reg_byte(MCP23017_GPIOB, int(self.param['InitValB'], 0))

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('20', '21', '22', '23', '24', '25', '26', '27')

# -----

    def variables(self, news:dict):
        if not self._i2c:
            return

        try:
            for key, reg in (('TrigVarA', MCP23017_GPIOA), ('TrigVarB', MCP23017_GPIOB)):
                name = self.param[key]
                if name and name in news:
                    val = Variable.get(name)
                    if type(val) == str:
                        val = int(val, 0)
                    if 0 <= val <= 255:
                        self._i2c.write_reg_byte(reg, val)

        except Exception as e:
            print(str(e))
            self._last_error = str(e)

# -----

    def timer(self, prepare:bool):
        if not self._i2c:
            return

        try:
            for key, reg in (('RespVarA', MCP23017_GPIOA), ('RespVarB', MCP23017_GPIOB)):
                name = self.param[key]
                if name:
                    val = self._i2c.read_reg_byte(reg)
                    print(val)
                    if val != self._last_val:
                        self._last_val = val
                        Variable.set(name, val)

        except Exception as e:
            print(str(e))
            self._last_error = str(e)

#######
