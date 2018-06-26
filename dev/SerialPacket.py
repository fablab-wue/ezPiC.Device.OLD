



class SerialPacketBase():
    def __init__(self, min_size):
        self._min_len = min_size
        self._data = bytearray()
        self._param = {}
        pass

    def add_data(self, data:bytes):
        self._data.extend(data)

    def process(self):
        while len(self._data) >= self._min_len:
            if self._is_valid():
                ret = self._interpret()
                return ret
            self._remove_data(1)
        return None

    def set_param(self, param):
        self._param.update(param)
        pass

    def _is_valid(self):
        if self._data[13] != 0x0A:   # '\n'
            return False
        if self._data[12] != 0x0D:   # '\r'
            return False
        for i in range(12):
            if (self._data[i] & 0xF0) != 0x30:
                return False
        return True

    def _interpret(self):
        val = (self._data[1] & 0x0F)
        val *= 10
        val += (self._data[2] & 0x0F)
        val *= 10
        val += (self._data[3] & 0x0F)
        val *= 10
        val += (self._data[4] & 0x0F)
        val *= 10
        val += (self._data[5] & 0x0F)

        scale = (self._data[0] & 0x07)
        mode = (self._data[6] & 0x0F)
        if self._data[7] & 0x04:   # neg
            val = -val

        unit = ''
        if mode == 0x0:   # A
            val *= 10**(scale-3)  
        elif mode == 0x1:   # Diode
            val *= 10**(scale-2)  
        elif mode == 0x2:   # Hz %
            val *= 10**(scale-2)  
        elif mode == 0x3:   # Ohm
            val *= 10**(scale-2)
            unit = 'Ohm'
        elif mode == 0x4:   # °C
            val *= 10**(scale-2)  
        elif mode == 0x5:   # Beep
            val *= 10**(scale-2)  
        elif mode == 0x6:   # F
            val *= 10**(scale-6)  
        elif mode == 0x9:   # A
            val *= 10**(scale-3)  
        elif mode == 0xB:   # V
            if scale == 4:   # mV
                val *= 10**(-2)
                unit = 'mV'
            else:
                val *= 10**(scale-4)  
                unit = 'V'
        elif mode == 0xD:   # uA
            val *= 10**(scale-2)  
        elif mode == 0xE:   # ADP
            val *= 10**(scale-2)  
        elif mode == 0xF:   # mA
            val *= 10**(scale-3)  
        else:
            pass

        if self._data[10] & 0x08:   # DC
            unit += '='
        if self._data[10] & 0x04:   # AC
            unit += '~'
        if self._data[9] & 0x04:   # max
            unit += 'max'
        if self._data[9] & 0x02:   # min
            unit += 'min'


        print(val, unit)
        self._remove_data(self._min_len)
        return val

    def _remove_data(self, size):
        self._data = self._data[size:]      