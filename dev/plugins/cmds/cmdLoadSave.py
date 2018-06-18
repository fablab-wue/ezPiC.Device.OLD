"""
Command Plugin for Load and Save Parameters
"""
from com.Globals import *

import dev.Device as Device
import dev.Gadget as Gadget
import dev.Gateway as Gateway
import dev.Rule as Rule
import dev.Machine as Machine
import dev.Cmd as Cmd

CONFIG_FILE = 'ezPiC.set'

#######

@Cmd.route('save')
def cmd_system_save(cmd:dict) -> tuple:
    """ saves all configuration and parameters of the plugins to cezPiC.set """

    err = None

    with open(CONFIG_FILE, 'w') as outfile:
        try:
            save_dict = {}
            Device.save(save_dict)
            Machine.save(save_dict)
            Gadget.save(save_dict)
            Gateway.save(save_dict)
            Rule.save(save_dict)
            # add other stuff like Gateway
            if MICROPYTHON:
                json.dump(save_dict, outfile)
            else:
                json.dump(save_dict, outfile, indent=2)
        except Exception as e:
            return (-100, 'Error on collectin save values - ' + str(e))

    return (0, None)

#######

@Cmd.route('load')
def cmd_system_load(cmd:dict) -> tuple:
    """ loads all configuration and parameters of the plugins from ezPiC.set """

    try:
        with open(CONFIG_FILE, 'r') as infile:
            config_all = json.load(infile)
            Device.load(config_all)
            Machine.load(config_all)
            Gadget.load(config_all)
            Gateway.load(config_all)
            Rule.load(config_all)
            # ...
    except FileNotFoundError as e:
        pass
    except Exception as e:
            return (-101, 'Error on collectin load values - ' + str(e))

    return (0, None)

#######
