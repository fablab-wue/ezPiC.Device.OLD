"""
Gadget Plugin for GPIO output
"""
from com.Globals import *

import dev.Gadget as Gadget
import dev.Variable as Variable
import dev.Machine as Machine
import dev.SerialPacket as SerialPacket

#######
# Globals:

EZPID = 'gdDmmMS8050'
PTYPE = PT_SENSOR
PNAME = 'DMM UNI-T UT61E ...Mastech/ELV MS8050'
PINFO = '???'

#######

class PluginGadget(Gadget.PluginGadgetBase):
    """ TODO """

    def __init__(self, module):
        super().__init__(module)
        self.param = {
            # must be params
            'NAME':PNAME,
            'ENABLE':False,
            'TIMER':0.1,
            # instance specific params
            'Port':'COM22',
            'RespVar':'DMM',
            }
        self._ser = None
        self._xxx = SerialPacket.SerialPacketBase(14)

# -----

    def init(self):
        super().init()

        try:
            #out = self._get_variable(key)
            id = self.param['Port']

            err, ret = Machine.get_handler_instance('UART', id)
            if not err:
                self._ser = ret
                self._ser.init(19200, 7, 1, 1) #19200-7-Odd-1
                self._ser.set_dtr(True)    # DTR-Pin to +
                self._ser.set_rts(False)   # RTS-Pin to -
            else:
                self._ser = None
        except Exception as e:
            self._ser = None

# -----

    def exit(self):
        super().exit()

# -----

    def get_features(self):
        features = {}
        err, ret = Machine.get_features('UART')
        if not err:
            features['UART'] = ret
        return features

# -----

    def timer(self, prepare:bool):
        if not self._ser:
            return
        
        nbytes = self._ser.any()
        if not nbytes:
            return

        try:
            data = self._ser.read(nbytes)
            self._xxx.add_data(data)
            while True:
                x = self._xxx.process()
                if not x:
                    break
                #print(x)
                
            name = self.param['RespVar']
        except:
            pass

# =====

#######
