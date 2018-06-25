



class SerialPacketBase():
    def __init__(self, min_size):
        self._min_len = min_size
        self._data = bytearray()
        self._param = {}
        pass

    def add_data(self, data:bytes):
        pass

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
        return False

    def _interpret(self):
        self._remove_data(self._min_len)
        return None

    def _remove_data(self, size):
        return None        