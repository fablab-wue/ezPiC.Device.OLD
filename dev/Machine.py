"""
...TODO
"""
from com.Globals import *

import com.Tool as Tool
import dev.Timer as Timer

#######
# Globals:

_PLUGINDIR = 'dev/plugins/machines'
_MACHINEPLUGINS = {}
_MACHINES = []
_MACHINELOCK = RLock()
_MACHINETIMER = 0
_MACHINEFEATURES = {}
_MACHINEFEATURECLASSS = {}

#######

def init():
    """ Prepare module vars and load plugins """
    global _MACHINEPLUGINS

    plugins = Tool.load_plugins(_PLUGINDIR, 'ma')
    for plugin in plugins:
        try:
            _MACHINEPLUGINS[plugin.MAPID] = plugin
        except:
            pass


    err = None
    ret = None

    for mapid, module in _MACHINEPLUGINS.items():
        try:
            machine = module.PluginMachine(module)
            _MACHINES.append(machine)
            machine.init()
        except Exception as e:
            err = -1
            ret = str(e)

# =====

def run():
    """ TODO """
    global _MACHINEPLUGINS, _MACHINETIMER

#######

def load(config_all: dict):
    if not "machines" in config_all:
        return
    for config in config_all["machines"]:
        #mapid = config["MAPID"]
        #loaded_version = config["version"]
        params = config["params"]
        set_params(params)

# =====

def save(append: dict = None):
    ret = []
    with _MACHINELOCK:
        for machine in _MACHINES:
            try:
                config = {}
                config["MAPID"] = machine.module.MAPID
                config["version"] = machine.version
                config["params"] = machine.get_params()
                ret.append(config)
            except Exception as e:
                return (-1, str(e))

    if not append is None:
        append["machines"] = ret
        return (0, append)
    
    return (0, {"machines": ret})

#######

def get_plugin_list() -> tuple:
    """ TODO """
    pl = []

    with _MACHINELOCK:
        for mapid, module in _MACHINEPLUGINS.items():
            p = {}
            p['MAPID'] = module.MAPID
            p['PNAME'] = module.PNAME
            p['PINFO'] = module.PINFO
            p['PFILE'] = module.__name__
            pl.append(p)

    return (0, pl)

# =====

def get_list() -> tuple:
    """ TODO """
    dl = []

    with _MACHINELOCK:
        for idx, machine in enumerate(_MACHINES):
            d = {}
            d['idx'] = idx
            d['MAPID'] = machine.module.MAPID
            d['PNAME'] = machine.module.PNAME
            d['info'] = machine.get_info()
            dl.append(d)

    return (0, dl)

# =====

def get_params(key: str=None) -> tuple:
    """ TODO """
    ret = {}

    with _MACHINELOCK:
        try:
            for machine in _MACHINES:
                ret1 = machine.get_params(key)
                ret.update(ret1)
        except Exception as e:
            return (-1, str(e))

    return (0, ret)

# =====

def set_params(params: dict) -> tuple:
    """ TODO """
    ret = None

    with _MACHINELOCK:
        try:
            for machine in _MACHINES:
                machine.set_params(params)
        except Exception as e:
            return (-1, str(e))

    return (0, ret)

#######

def get_features(feature:str) -> tuple:
    """ TODO """
    if feature:
        return (0, _MACHINEFEATURES.get(feature, []))
    else:
        return (0, list(_MACHINEFEATURES))

# =====

def set_feature(feature:str, itemlist) -> tuple:
    """ TODO """
    _MACHINEFEATURES[feature] = itemlist
    return (0, None)

#######

def get_handler_class(feature:str) -> tuple:
    """ TODO """
    return (0, _MACHINEFEATURECLASSS.get(feature, None))

# =====

def set_handler_class(feature:str, handler_class) -> tuple:
    """ TODO """
    _MACHINEFEATURECLASSS[feature] = handler_class
    return (0, None)

# =====

def get_handler_instance(feature:str, id) -> tuple:
    """ TODO """
    try:
        pin_class = _MACHINEFEATURECLASSS.get(feature, None)
        if pin_class and id:
            inst = pin_class(id)
            return (0, inst)
        else:
            return (-666, 'Can not create instance')
    except Exception as e:
        return (-666, str(e))

#######

class PluginMachineBase():
    """ TODO """
    version = '1.0'

    def __init__(self, module):
        self.module = module
        self.param = {}

    def init(self):
        """ init a new instance after adding to task list or reinit an existing instance after loading/changing params """
        pass

    def exit(self):
        """ exit an existing instance after removing from task list """
        pass

    def get_info(self) -> str:
        """ get the description from the module """
        return str(self.param)

    def get_params(self, key:str=None):
        """ get the value for a given param key or get all key-value pairs as dict """
        if key:
            return self.param.get(key, None)
        else:
            return self.param

    def set_params(self, param_new:dict):
        """ updates the param key-value pairs with given dict """
        for key in self.param:
            if key in param_new and self.param[key] != param_new[key]:   # found any change?
                self.exit()
                for key in self.param:
                    if key in param_new:
                        self.param[key] = param_new[key]
                if self.param.get('ENABLE', False):
                    self.init()
                break

#######
# DEBUG

def pin(id, value) -> tuple:
    """ TODO """
    err, pin_class = get_handler_class('PIN_IO')
    if not err and pin_class:
        pin = pin_class(id, pin_class.OUT)
        if pin:
            if value:
                pin.set(int(value))
            else:
                return (0, pin.get())

    return (0, None)

#######

