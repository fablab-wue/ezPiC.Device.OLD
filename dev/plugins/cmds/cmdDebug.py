"""
Command Plugin for System Commands

"""
from com.Globals import *

import dev.Cmd as Cmd
import dev.Timer as Timer
import dev.Machine as Machine

#######

@Cmd.route('quit')
def cmd_quit(cmd:dict) -> tuple:
    """ exit program """
    log(LOG_ERROR, 'QUIT')
    RUN = False
    sys.exit(0)

    return (0, None)

#######

@Cmd.route('loglevel', 'level')
def cmd_loglevel(cmd:dict) -> tuple:
    """ set logging level """
    level = int(cmd.get('level', None))
    LOG_LEVEL = level

    return (0, None)

#######

@Cmd.route('clock')
def cmd_clock(cmd:dict) -> tuple:
    return (0, Timer.clock())

#######

@Cmd.route('mem')
def cmd_mem(cmd:dict) -> tuple:
    if MICROPYTHON:
        import micropython
        micropython.mem_info()   # print direct only :-(
    import gc
    gc.collect()
    f = gc.mem_free()
    return (0, f)

#######

@Cmd.route('machine.pin', 'id value')
def cmd_machine_pin(cmd:dict) -> tuple:
    """ gets featue for MACHINE instances (merged) """
    id = cmd.get('id', None)
    value = cmd.get('value', 0)
    err, ret = Machine.pin(id, value)

    return (err, ret)

#######
