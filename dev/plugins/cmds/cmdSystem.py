"""
Command Plugin for System Commands
"""
from com.Globals import *

import dev.Device as Device
import dev.Cmd as Cmd

#######

@Cmd.route('ping')
def cmd_ping(cmd:dict) -> tuple:
    """ tests communication - returns string 'pong' """
    log(LOG_DEBUG, 'Ping')

    return (0, 'pong')

#######

@Cmd.route('version')
def cmd_system_version(cmd:dict) -> tuple:
    """ gets the version of ezPiC """
    return (0, VERSION)

#######

@Cmd.route('about')
def cmd_system_about(cmd:dict) -> tuple:
    """ gets about information """
    return (0, 'ezPiC-Project by Jochen Krapf et al. - https://github.com/fablab-wue/ezPiC')

#######

@Cmd.route('commands')
def cmd_system_commands(cmd:dict) -> tuple:
    """ gets a list of all available commands with arguments """

    cl = []

    for cmd in Cmd.COMMANDS:
        cmd_str = cmd['command']
        if cmd['has_index']:
            cmd_str += '.<idx>'
        args = cmd['args']
        if args:
            for key in args:
                cmd_str += ' <' + key + '>'
        func = cmd['func']
        if not MICROPYTHON and func.__doc__:
            cmd_str += '   # ' + func.__doc__.replace('\n', ' ').strip()
        cl.append(cmd_str)

    return (0, cl)

#######

@Cmd.route('system.getparams')
@Cmd.route('device.getparams')
def cmd_syscongig_getparam(cmd:dict) -> tuple:
    """ gets params from the system configutation """
    err, ret = Device.get_params()

    return (err, ret)

#######

@Cmd.route('system.setparams', 'params')
@Cmd.route('device.setparams', 'params')
def cmd_syscongig_setparam(cmd:dict) -> tuple:
    """ sets params for the system configutation """
    params = cmd.get('params', None)
    err, ret = Device.set_params(params)

    return (err, ret)

#######

