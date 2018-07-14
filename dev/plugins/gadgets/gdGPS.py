"""
Gadget Plugin for Pulse Counter with UART
Based on ???
"""
from micropyGPS import MicropyGPS

from com.Globals import *

import dev.Gadget as Gadget
from dev.GadgetSerial import PluginGadgetSerial as GS
import dev.Variable as Variable
import dev.Machine as Machine

#######
# Globals:

EZPID = 'gdGPSUART'
PTYPE = PT_SENSOR
PNAME = 'GPS NMEA (UART)'
PINFO = ''

#######

class PluginGadget(GS):
    """ TODO """

    def __init__(self, module):
        super().__init__(module, 9)   # 9 byte data packet
        self.param = {
            # must be params
            'NAME':PNAME,
            'ENABLE':False,
            'TIMER':0,
            'PORT':'',
            # instance specific params
            'RespVarLat':'GPS.Latitude',
            'RespVarLon':'GPS.Longitude',
            'RespVarCrs':'GPS.Course',
            'RespVarAlt':'GPS.Altitude',
            'RespVarSpd':'GPS.Speed',
            }
        self._gps = MicropyGPS()

# -----

    def init(self):
        super().init()

        if self._ser:
            self._ser.init(9600, 8, None, 1) # baud=9600 databits=8 parity=none stopbits=1

# -----

    def exit(self):
        super().exit()

# -----

    def idle(self):
        if not self._ser:
            return

        while self._ser.any():
            data = self._ser.read()
            data = data.decode()
            sentence = self._gps.update(data)
            if sentence:
                print(sentence)
                lat = self._gps.latitude
                lon = self._gps.longitude
                alt = self._gps.altitude
                crs = self._gps.course
                spd = self._gps.speed
                if sentence == 'GPRMC':
                    source = self.param['NAME']

                    key = self.param['RespVarLat']
                    if key:
                        value = lat[0] + lat[1]/60
                        if lat[2] == 'S':
                            value = -value
                        Variable.set(key, value, source, '°', '{:.6f}')

                    key = self.param['RespVarLon']
                    if key:
                        value = lon[0] + lon[1]/60
                        if lon[2] == 'W':
                            value = -value
                        Variable.set(key, value, source, '°', '{:.6f}')
                        
                    key = self.param['RespVarAlt']
                    if key:
                        Variable.set(key, alt, source, 'm', '{:.1f}')
                        
                    key = self.param['RespVarCrs']
                    if key:
                        Variable.set(key, crs, source, '°', '{:.1f}')
                        
                    key = self.param['RespVarSpd']
                    if key:
                        Variable.set(key, spd, source)    # Tuple!!!
                        
                    pass
                    

# -----

    def timer(self, prepare:bool):
        pass
            
# =====


#######
