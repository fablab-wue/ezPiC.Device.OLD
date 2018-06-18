"""
Command Plugin for Info Commands
"""
from com.Globals import *

import dev.Device as Device
import dev.Cmd as Cmd

#######

@Cmd.route('info')
def cmd_system_info(cmd:dict) -> tuple:
    """ gets common information about the system and the environment """
    i = {}
    i['software.name'] = 'ezPiC'
    i['software.version'] = VERSION
    i['command.source'] = cmd['SRC']

    try:
        i['sys.version'] = sys.version
        i['sys.platform'] = sys.platform
        i['sys.implementation.name'] = sys.implementation.name
        #i['sys.maxsize'] = sys.maxsize
    except:
        pass

    try:
        import platform
        i['platform.node'] = platform.node()
        i['platform.system'] = platform.system()
        i['platform.release'] = platform.release()
        i['platform.version'] = platform.version()
        i['platform.machine'] = platform.machine()
        i['platform.processor'] = platform.processor()
        i['platform.architecture'] = platform.architecture()
        i['platform.dist'] = platform.dist()
        i['platform.python_version'] = platform.python_version()
    except:
        pass

    try:
        import gc
        i['gc.mem_free'] = gc.mem_free()
    except:
        pass

    return (0, i)

#######
