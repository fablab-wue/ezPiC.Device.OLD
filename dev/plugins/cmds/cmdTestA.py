"""
Command Plugin for Testing
"""
from com.Globals import *

import dev.Cmd as Cmd

#######

@Cmd.route('xxx.#', 'a b c')
def cmd_xxx(cmd:dict) -> tuple:
    """ TESTING """
    x = cmd.get('a', '0')

    return (0, None)

#######

@Cmd.route(r'b')
def cmd_b(cmd:dict) -> tuple:
    """ TESTING """
    log(LOG_DEBUG, 'cmdB ' + str(cmd))
    x = cmd.get('x', '0')
    return (0, 'b')

#######
