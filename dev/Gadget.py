"""
...TODO
"""
from com.Globals import *

import com.Tool as Tool
import dev.Timer as Timer

#######
# Globals:

_PLUGINDIR = 'dev/plugins/gadgets'
_GADGETPLUGINS = {}
_GADGETS = []
_GADGETLOCK = RLock()
_GADGETTIMER = 0

#######

def gadget_timer_handler(news, args):
    global _GADGETS, _GADGETTIMER

    with _GADGETLOCK:
        t = Timer.clock()

        for idx, gadget in enumerate(_GADGETS):
            if gadget.is_enabled():
                if gadget.prepare_next and (t >= gadget.prepare_next):
                    gadget.prepare_next = None
                    gadget.timer(True)

                if gadget.timer_next and (t >= gadget.timer_next):
                    if gadget.timer_period: # cyclic timer
                        gadget.timer_next += gadget.timer_period
                        if gadget.timer_next < t: # missed some events
                            gadget.timer_next = t + gadget.timer_period
                        if gadget.prepare_time:
                            gadget.prepare_next = gadget.timer_next - gadget.prepare_time
                    else: # singel event
                        gadget.timer_next = None
                    gadget.timer(False)
                #else: # disabled
                #gadget.timer_next = None

                if news:
                    gadget.variables(news)

        for gadget in _GADGETS:
            if gadget.is_enabled():
                gadget.idle()

#######

def init():
    """ Prepare module vars and load plugins """
    global _GADGETPLUGINS

    plugins = Tool.load_plugins(_PLUGINDIR, 'gd')
    for plugin in plugins:
        try:
            _GADGETPLUGINS[plugin.EZPID] = plugin
        except:
            pass

# =====

def run():
    """ TODO """
    global _GADGETPLUGINS, _GADGETTIMER

    Timer.register_cyclic_handler(gadget_timer_handler)

#######

def load(config_all:dict):
    if not "gadgets" in config_all:
        return
    for config in config_all["gadgets"]:
        try:
            ezPID = config["EZPID"]
            loaded_version = config["version"]
            params = config["params"]
            err, idx = add(ezPID, params)
            running_version = _GADGETS[idx].version

            if not err and loaded_version != running_version:
                log(LOG_WARN, "task " +  ezPID + " has change version form " + loaded_version + " to " + running_version)
        except Exception as e:
            pass

# =====

def save(append:dict = None):
    ret = []
    with _GADGETLOCK:
        for gadget in _GADGETS:
            try:
                config = {}
                config["EZPID"] = gadget.module.EZPID
                config["version"] = gadget.version
                config["params"] = gadget.get_params()
                ret.append(config)
            except Exception as e:
                return (-1, str(e))

    if not append is None:
        append["gadgets"] = ret
        return (0, append)
    
    return (0, {"gadgets":ret})

#######

def add(plugin_id:str, params:dict = None) -> tuple:
    """ TODO """
    with _GADGETLOCK:
        try:
            module = _GADGETPLUGINS.get(plugin_id, None)
            if module:
                gadget = module.PluginGadget(module)
                _GADGETS.append(gadget)
                ret = len(_GADGETS) - 1
                if params:
                    gadget.set_params(params)
                return (0, ret)
            else:
                return (-1, 'Unknown EZPID')
        except Exception as e:
            return (-1, str(e))

# =====

def delete(idx:int) -> tuple:
    """ TODO """
    with _GADGETLOCK:
        try:
            gadget = _GADGETS[idx]
            gadget.exit()
            del _GADGETS[idx]
        except Exception as e:
            return (-1, str(e))

    return (0, None)

# =====

def clear() -> tuple:
    """ TODO """
    global _GADGETS

    with _GADGETLOCK:
        for gadget in _GADGETS:
            try:
                gadget.exit()
            except Exception as e:
                return (-1, str(e))
        _GADGETS = []

    return (0, None)

# =====

def get_plugin_list() -> tuple:
    """ TODO """
    pl = []

    with _GADGETLOCK:
        for ezPID, module in _GADGETPLUGINS.items():
            p = {}
            p['EZPID'] = module.EZPID
            p['PNAME'] = module.PNAME
            p['PFILE'] = module.__name__
            pl.append(p)

    return (0, pl)

# =====

def get_list() -> tuple:
    """ TODO """
    dl = []

    with _GADGETLOCK:
        for idx, gadget in enumerate(_GADGETS):
            d = {}
            d['idx'] = idx
            d['EZPID'] = gadget.module.EZPID
            d['PNAME'] = gadget.module.PNAME
            d['NAME'] = gadget.get_name()
            d['ENABLE'] = gadget.get_params('ENABLE')
            d['info'] = gadget.get_info()
            dl.append(d)

    return (0, dl)

# =====

def get_params(idx:int, key:str=None) -> tuple:
    """ TODO """
    with _GADGETLOCK:
        try:
            gadget = _GADGETS[idx]
            return (0, gadget.get_params(key))
        except Exception as e:
            return (-1, str(e))

# =====

def set_params(idx:int, params:dict) -> tuple:
    """ TODO """
    with _GADGETLOCK:
        try:
            gadget = _GADGETS[idx]
            return (0, gadget.set_params(params))
        except Exception as e:
            return (-1, str(e))

# =====

def get_features(idx:int) -> tuple:
    """ TODO """
    with _GADGETLOCK:
        try:
            gadget = _GADGETS[idx]
            return (0, gadget.get_features())
        except Exception as e:
            return (-1, str(e))

# =====

def get_html(idx:int) -> tuple:
    """ TODO """
    with _GADGETLOCK:
        try:
            gadget = _GADGETS[idx]
            return (0, gadget.get_html())
        except Exception as e:
            return (-1, str(e))

#######

class PluginGadgetBase():
    """ TODO """
    version = '1.0'

    def __init__(self, module):
        self.module = module
        self.param = {}
        self.timer_next = 0
        self.timer_period = 0
        self.prepare_next = 0
        self.prepare_time = 0

    def init(self):
        """ init a new instance after adding to task list or reinit an existing instance after loading/changing params """
        self.timer_next = 0
        self.prepare_next = 0
        self.timer_period = 0
        
        t = self.param.get('TIMER', None)
        if t:
            t = int(float(t) * 1000)
            if t > 0:
                self.timer_period = t
        if self.timer_period and self.is_enabled():
            self.timer_next = Timer.clock() + self.timer_period
            if self.prepare_time:
                self.prepare_next = self.timer_next - self.prepare_time

    def exit(self):
        """ exit an existing instance after removing from task list """
        pass

    def is_enabled(self) -> bool:
        """ get enable status """
        return self.param['ENABLE']

    def get_name(self) -> str:
        """ get the name from the module """
        return self.param.get('NAME', 'Unknown')

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
                if self.is_enabled():
                    self.init()
                break

    def get_features(self):
        """ get the features as dict """
        return {}

    def get_html(self) -> str:
        """ get the html template name from the module """
        name = self.module.EZPID.split('_', 1)[0]
        return 'web/www/gadgets/{}.html'.format(name)

    def idle(self):
        return None

    def timer(self, prepare:bool):
        return None

    def variables(self, news:dict):
        pass

#######
