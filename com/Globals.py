"""
Commen Module to be loaded in all project modules
"""
try:   # try MicroPython
    import uos as os
    MICROPYTHON = True
except:   # CPython
    MICROPYTHON = False

if MICROPYTHON:
    import ujson as json
    from _thread import allocate_lock as RLock
else:   # CPython
    import os
    import json
    from threading import RLock

    def const(x):
        return x

import sys
import time

RUN = True
VERSION = '0.0.?'

CNF = {}


######## 

LOG_ERROR       = const(1)
LOG_WARN        = const(2)
LOG_INFO        = const(3)
LOG_DEBUG       = const(4)
LOG_EXT_DEBUG   = const(5)

LOG_LEVEL = LOG_DEBUG   # 0=NoOutput, 1=Error, 2=Warning, 3=Info, 4=Debug, 5=Ext.Debug
    
# -----

def log(level:int, msg:str, *args):
    global LOG_LEVEL

    if level > LOG_LEVEL:
        return

    if args:
        msg = msg.format(*args)

    now_str = time_to_str(time.time())
    msg = '{0} [{1}] {2}'.format(now_str, level, msg)
    
    if CNF['logFile']:
        with open(CNF['logFile'], 'a') as f:
            f.write(msg)
    else:
        print(msg)

#######

def time_to_str(t:time) -> str:
    time_t = time.localtime(t)
    t_str = "%04d-%02d-%02d %02d:%02d:%02d" % time_t[0:6]
    return t_str

########

