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
import math

#######
# Globals:

EZPID = 'gdGPSUART'
PTYPE = PT_SENSOR
PNAME = 'GPS - NMEA (serial)'

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
            'RespVarPos':'GPS.Position',
            'RespVarLat':'GPS.Latitude',
            'RespVarLon':'GPS.Longitude',
            'RespVarCrs':'GPS.Course',
            'RespVarAlt':'GPS.Altitude',
            'RespVarSpd':'GPS.Speed',
            }
        self._gps = MicropyGPS(local_offset=0, location_formatting='ddm')

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
                #print(sentence, self._gps.timestamp)
                if sentence == 'GPRMC' and self._gps.valid:
                    source = self.param['NAME']

                    #print(sentence, self._gps.timestamp, self._gps.local_offset)
                    
                    key = self.param['RespVarPos']
                    if key:
                        lat = self._gps.latitude
                        lon = self._gps.longitude
                        pos = '{:d}°{:02d}\'{:02.1f}"{} {:d}°{:02d}\'{:02.1f}"{}'.format(lat[0], int(lat[1]), math.modf(lat[1])[0]*60.0, lat[2], lon[0], int(lon[1]), math.modf(lon[1])[0]*60.0, lon[2])
                        #pos = self._gps.latitude_string() + ' ' + self._gps.longitude_string()
                        Variable.set(key, pos, source)

                    key = self.param['RespVarLat']
                    if key:
                        lat = self._gps.latitude
                        value = lat[0] + lat[1]/60
                        if lat[2] == 'S':
                            value = -value
                        Variable.set(key, value, source, '°', '{:.6f}')

                    key = self.param['RespVarLon']
                    if key:
                        lon = self._gps.longitude
                        value = lon[0] + lon[1]/60
                        if lon[2] == 'W':
                            value = -value
                        Variable.set(key, value, source, '°', '{:.6f}')
                        
                    key = self.param['RespVarAlt']
                    if key:
                        alt = self._gps.altitude
                        Variable.set(key, alt, source, 'm', '{:.1f}')
                        
                    key = self.param['RespVarCrs']
                    if key:
                        crs = self._gps.course
                        Variable.set(key, crs, source, '°', '{:.1f}')
                        
                    key = self.param['RespVarSpd']
                    if key:
                        spd = self._gps.speed[2]
                        Variable.set(key, spd, source, 'km/h', '{:.3f}')

# -----

    def timer(self, prepare:bool):
        pass
            
# =====


#######
