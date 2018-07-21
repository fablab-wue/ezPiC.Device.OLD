"""
Gadget Plugin for DFPlayer Mini and YX5300
Based on ???
"""
from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdMP3Ser'
PTYPE = PT_SENSOR
PNAME = 'MP3 Notification (serial)'
PINFO = '?'

#######

class PluginGadget(GS):
    """ TODO """

    def __init__(self, module):
        super().__init__(module, 10)   # 10 byte data packet
        self.param = {
            # must be params
            'NAME':PNAME,
            'ENABLE':False,
            'TIMER':0,
            'PORT':'',
            # instance specific params
            'TrigVar':'CMD.Notify',
            'Volume':30,
            'Mode':0,
            'Media':-1,
            }

# -----

    def init(self):
        super().init()

        if self._ser:
            self._ser.init(9600, 8, None, 1) # baud=9600 databits=8 parity=none stopbits=1

            self.param['Mode'] = int(self.param['Mode'])
            self.set_volume(int(self.param['Volume']))   # Set volume
            self.set_media(int(self.param['Media']))   # Set media SD/USB
            #self.play_index(1)   # Play

# -----

    def exit(self):
        super().exit()

# -----

    def variables(self, news:dict):
        try:
            key = self.param['TrigVar']
            if key in news:
                val = news.get(key, 1)

                if type(val) is str:
                    if val.find(':') > 0:
                        val = val.split(':', 1)
                        ndir = int(val[0])
                        file = int(val[1])
                        self.play_folder(ndir, file)   # Play Folder
                    else:
                        val = int(val)
                        self.play_index(val)   # Play Index
                elif type(val) is int:
                    self.play_index(val)   # Play Index
        except:
            pass

# =====

    def send_command_long(self, cmd:int, val:int, nlen=10):
        #nlen = 10   # 8 or 10
        buf = bytearray(nlen)

        buf[0] = 0x7E
        buf[1] = 0xFF
        buf[2] = 0x06
        buf[3] = cmd
        buf[4] = 0
        buf[5] = (val >> 8) & 0xFF
        buf[6] = val & 0xFF
        buf[7] = 0xEF

        if nlen == 10:
            sum = 0
            for i in range(1, 7):
                sum -= buf[i]
            buf[7] = (sum >> 8) & 0xFF
            buf[8] = sum & 0xFF
            buf[9] = 0xEF

        if self._ser:
            self._ser.write(buf)

# -----

    def send_command_short(self, cmd:int, val:int, nlen=6):
        buf = bytearray(nlen)

        buf[0] = 0x7E
        buf[1] = nlen-2
        buf[2] = cmd
        if nlen == 6:
            buf[3] = (val >> 8) & 0xFF
            buf[4] = val & 0xFF
            buf[5] = 0xEF
        else:
            buf[3] = val & 0xFF
            buf[4] = 0xEF

        if self._ser:
            self._ser.write(buf)

# -----

    def play_index(self, val:int):
        if not 1 <= val <= 3000:
            return
        if self.param['Mode'] == 3:
            self.send_command_short(0x41, val)   # Play
        if self.param['Mode'] == 2:
            self.send_command_long(0x03, val, 8)   # Play
        else:
            self.send_command_long(0x03, val)   # Play

# -----

    def play_folder(self, ndir:int, file:int):
        if not 1 <= ndir <= 99:
            return
        if not 1 <= file <= 255:
            return
        val = ndir << 8 | file
        if self.param['Mode'] == 3:
            self.send_command_short(0x42, val)   # Play Folder
        if self.param['Mode'] == 2:
            self.send_command_long(0x0F, val, 8)   # Play Folder
        else:
            self.send_command_long(0x0F, val)   # Play Folder

# -----

    def set_volume(self, val:int):
        if not 0 <= val <= 30:
            return
        if self.param['Mode'] == 3:
            self.send_command_short(0x31, val, 5)   # Set volume
        if self.param['Mode'] == 2:
            self.send_command_long(0x06, val, 8)   # Set volume
        else:
            self.send_command_long(0x06, val)   # Set volume

# -----

    def set_media(self, val:int):
        if not 0 <= val <= 4:
            return
        if self.param['Mode'] == 3:
            self.send_command_short(0x35, val, 5)   # Set volume
        if self.param['Mode'] == 2:
            self.send_command_long(0x09, val, 8)   # Set volume
        else:
            self.send_command_long(0x09, val)   # Set volume

#######
