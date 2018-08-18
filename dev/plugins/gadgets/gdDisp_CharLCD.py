"""
Gadget Plugin for Char LCD
Based on: http://abyz.me.uk/rpi/pigpio/examples.html#Python%20code 
File: abyz.me.uk/rpi/pigpio/code/i2c_lcd_py.zip

This class provides simple functions to display text on an I2C LCD
based on the PCF8574T I2C 8-bit port expander.

PCF8574T P7   P6   P5   P4   P3   P2   P1   P0
HD44780  B7   B6   B5   B4   BL   E    RW   RS

"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetI2C import PluginGadgetI2C as GI2C
import dev.Variable as Variable
import dev.Machine as Machine
#import com.Tool as Tool
import time

#######
# Globals:

EZPID = 'gdCharLCD'
PTYPE = PT_SENSOR | PT_ACTUATOR
PNAME = '@WORK Disp.Text - HD44780 over PCF8574 - Char.LCD Display with Adapter (I2C)'

#######

class PluginGadget(GI2C):
    """ TODO """
    _LCD_ROW = [0x80, 0xC0, 0x94, 0xD4]

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':'CharLCD',
            'ENABLE':False,
            'TIMER':3,
            'PORT':'1',
            'ADDR':'3F',
            # instance specific params
            'Lines':'4',
            'CPL':'20',
            'Text':'Hello',
            }
        self._last_text = {}

# -----

    def init(self):
        super().init()

        #if self._i2c and self.param['InitVal']:
        #    self._i2c.write_byte(int(self.param['InitVal'], 0))

        self.width = 20
        self.rows = 4
        self.backlight_on = True
        self._last_text = {}

        self.RS = (1<<0)
        self.E  = (1<<2)
        self.BL = (1<<3)
        self.B4 = 4

        #self._h = pi.i2c_open(bus, addr)

        self._init()

        self.put_line(0, "-ezPiC-")


# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        return super().get_features()

# -----

    def get_addrs(self):
        return ('27', '3F')

# -----

    def timer(self, prepare:bool):
        text = self.param['Text']
        if text:
            text = Variable.texter(text)

            lines = text.replace('\r', '').split('\n')
            while len(lines) < self.rows:
                lines.append('')
            for i, line in enumerate(lines):
                if line != self._last_text.get(i, None):
                    self._last_text[i] = line
                    self.put_line(i, line)

# =====

    def backlight(self, on):
        """
        Switch backlight on (True) or off (False).
        """
        self.backlight_on = on

    def _init(self):

        self._inst(0x33) # Initialise 1
        time.sleep(0.01)
        self._inst(0x33) # Initialise 1
        time.sleep(0.01)
        self._inst(0x32) # Initialise 2
        time.sleep(0.01)
        self._inst(0x28) # 4-bits, 1 line, 5x8 font
        time.sleep(0.01)
        self._inst(0x06) # Cursor increment
        time.sleep(0.01)
        self._inst(0x0C) # Display on,move_to off, blink off 
        time.sleep(0.01)
        self._inst(0x01) # Clear display

    def _byte(self, MSb, LSb):

        if self.backlight_on:
            MSb |= self.BL
            LSb |= self.BL

        self._i2c.write_buffer([MSb | self.E, MSb & ~self.E, LSb | self.E, LSb & ~self.E])

    def _inst(self, bits):

        MSN = (bits>>4) & 0x0F
        LSN = bits & 0x0F

        MSb = MSN << self.B4
        LSb = LSN << self.B4

        self._byte(MSb, LSb)

    def _data(self, bits):

        MSN = (bits>>4) & 0x0F
        LSN = bits & 0x0F

        MSb = (MSN << self.B4) | self.RS
        LSb = (LSN << self.B4) | self.RS

        self._byte(MSb, LSb)

    def move_to(self, row, column):
        """
        Position cursor at row and column (0 based).
        """
        self._inst(self._LCD_ROW[row]+column)

    def put_inst(self, byte):
        """
        Write an instruction byte.
        """
        self._inst(byte)

    def put_symbol(self, index):
        """
        Write the symbol with index at the current cursor postion
        and increment the cursor.
        """
        self._data(index)

    def put_chr(self, char):
        """
        Write a character at the current cursor postion and
        increment the cursor.
        """
        self._data(ord(char))

    def put_str(self, text):
        """
        Write a string at the current cursor postion.  The cursor will
        end up at the character after the end of the string.
        """
        for i in text:
            self.put_chr(i)

    def put_line(self, row, text):
        """
        Replace a row (0 based) of the LCD with a new string.
        """
        text = text.ljust(self.width)[:self.width]

        self.move_to(row, 0)

        self.put_str(text)


#######
