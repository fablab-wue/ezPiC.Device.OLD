"""
TODO
Infos about DMM protocols:
https://www-user.tu-chemnitz.de/~heha/hs/UNI-T/
http://www.mtoussaint.de/qtdmm.html#download
https://usermanual.wiki/Document/124411in01enProtocolRev2VC650BTDESKTOPDMM.2818719350
https://sigrok.org/wiki/Main_Page
https://sigrok.org/wiki/Multimeter_comparison
"""
from com.Globals import *

import dev.Gadget as Gadget
#import dev.Variable as Variable
import dev.Machine as Machine


class PluginGadgetSerial(Gadget.PluginGadgetBase):
    """ TODO """
    Pow10 = { -10:0.0000000001, -9:0.000000001, -8:0.00000001, -7:0.0000001, -6:0.000001, -5:0.00001, -4:0.0001, -3:0.001, -2:0.01, -1:0.1, 0:1.0, 1:10.0, 2:100.0, 3:1000.0, 4:10000.0, 5:100000.0, 6:1000000.0, 7:10000000.0, 8:100000000.0, 9:1000000000.0, 10:10000000000.0 }

    def __init__(self, module, packet_size):
        super().__init__(module)
        self.packet_size = packet_size
        self.data = bytearray()
        self._ser = None
        
        self.value = 0.0
        self.unit = ''
        self.form = ''

# -----

    def init(self):
        super().init()

        try:
            id = self.param['PORT']

            err, ret = Machine.get_handler_instance('UART', id)
            if not err:
                self._ser = ret
            else:
                self._ser = None
        except Exception as e:
            self._ser = None

# -----

    def exit(self):
        super().exit()
        if self._ser:
            self._ser.deinit()
            self._ser = None

# -----

    def get_features(self):
        features = {}
        err, ret = Machine.get_features('UART')
        if not err:
            features['UARTS'] = ret
        features['PNAME'] = self.module.PNAME
        return features

# =====

    def _remove_data(self, size):
        self.data = self.data[size:]

# -----

    def add_data(self, data:bytes):
        self.data.extend(data)

# -----

    def process(self):
        if not self._ser:
            return False
        
        nbytes = self._ser.any()
        if nbytes:
            sdata = self._ser.read(nbytes)
            self.add_data(sdata)

        while len(self.data) >= self.packet_size:
            if self.is_valid():
                self.interpret()
                return True
            self._remove_data(1)
        return False

# =====

    def is_valid(self):
        # HAVE TO BE DERIVED
        return False

# -----

    def interpret(self):
        # HAVE TO BE DERIVED
        return None

#######
