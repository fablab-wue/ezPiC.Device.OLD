"""
...TODO
"""
from com.Globals import *

import com.Tool as Tool
import dev.Timer as Timer

#######
# Globals:

_PLUGINDIR = 'dev/plugins/gateways'
_GATEWAYPLUGINS = {}
_GATEWAYS = []
_GATEWAYLOCK = RLock()
_GATEWAYTIMER = 0

#######

def gateway_timer_handler(news, args):
    global _GATEWAYS, _GATEWAYTIMER

    with _GATEWAYLOCK:
        t = Timer.clock()

        for idx, gateway in enumerate(_GATEWAYS):
            if gateway.timer_next and (t >= gateway.timer_next):
                if gateway.get_params('enable'):
                    if gateway.timer_period:   # cyclic timer
                        gateway.timer_next += gateway.timer_period
                        if gateway.timer_next < t:   # missed some events
                            gateway.timer_next = t + gateway.timer_period
                    else:   # singel event
                        gateway.timer_next = None
                    gateway.timer()
                else:   # disabled
                    gateway.timer_next = None

            if news:
                if gateway.get_params('enable'):
                    gateway.variables(news)

#######

def init():
    """ Prepare module vars and load plugins """
    global _GATEWAYPLUGINS

    plugins = Tool.load_plugins(_PLUGINDIR, 'gw')
    for plugin in plugins:
        try:
            _GATEWAYPLUGINS[plugin.GWPID] = plugin
        except:
            pass

# =====

def run():
    """ TODO """
    global _GATEWAYPLUGINS, _GATEWAYTIMER

    Timer.register_cyclic_handler(gateway_timer_handler)

#######

def load(config_all: dict):
    if not "gateways" in config_all:
        return
    for config in config_all["gateways"]:
        gwpid = config["GWPID"]
        loaded_version = config["version"]
        params = config["params"]
        err, idx = add(gwpid, params)
        running_version = _GATEWAYS[idx].version

        if not err and loaded_version != running_version:
            log(LOG_WARN, "task " +  gwpid + " has change version form " + loaded_version + " to " + running_version)

# =====

def save(append: dict = None):
    ret = []
    with _GATEWAYLOCK:
        for gateway in _GATEWAYS:
            try:
                config = {}
                config["GWPID"] = gateway.module.GWPID
                config["version"] = gateway.version
                config["params"] = gateway.get_params()
                ret.append(config)
            except Exception as e:
                return (-1, str(e))

    if not append is None:
        append["gateways"] = ret
        return (0, append)
    
    return (0, {"gateways": ret})

#######

def add(plugin_id: str, params: dict = None) -> tuple:
    """ TODO """
    with _GATEWAYLOCK:
        try:
            module = _GATEWAYPLUGINS.get(plugin_id, None)
            if module:
                gateway = module.PluginGateway(module)
                _GATEWAYS.append(gateway)
                ret = len(_GATEWAYS) - 1
                if params:
                    gateway.set_params(params)
                else:
                    gateway.init()
                return (0, ret)
            else:
                return (-1, 'Unknown GWPID')
        except Exception as e:
            return (-1, str(e))


# =====

def delete(idx: int) -> tuple:
    """ TODO """
    with _GATEWAYLOCK:
        try:
            gateway = _GATEWAYS[idx]
            gateway.exit()
            del _GATEWAYS[idx]
            return (0, None)
        except Exception as e:
            return (-1, str(e))


# =====

def clear() -> tuple:
    """ TODO """
    global _GATEWAYS

    with _GATEWAYLOCK:
        for gateway in _GATEWAYS:
            try:
                gateway.exit()
            except Exception as e:
                return (-1, str(e))
        _GATEWAYS = []

    return (0, None)

# =====

def get_plugin_list() -> tuple:
    """ TODO """
    pl = []

    with _GATEWAYLOCK:
        for gwpid, module in _GATEWAYPLUGINS.items():
            p = {}
            p['GWPID'] = module.GWPID
            p['PNAME'] = module.PNAME
            p['PINFO'] = module.PINFO
            p['PFILE'] = module.__name__
            pl.append(p)

    return (0, pl)

# =====

def get_list() -> tuple:
    """ TODO """
    gl = []

    with _GATEWAYLOCK:
        for idx, gateway in enumerate(_GATEWAYS):
            g = {}
            g['idx'] = idx
            g['GWPID'] = gateway.module.GWPID
            g['PNAME'] = gateway.module.PNAME
            g['name'] = gateway.get_name()
            g['enable'] = gateway.get_params('enable')
            g['info'] = gateway.get_info()
            gl.append(g)

    return (0, gl)

# =====

def get_params(idx: int, key: str=None) -> tuple:
    """ TODO """
    with _GATEWAYLOCK:
        try:
            gateway = _GATEWAYS[idx]
            return (0, gateway.get_params(key))
        except Exception as e:
            return (-1, str(e))

# =====

def set_params(idx: int, params: dict) -> tuple:
    """ TODO """
    with _GATEWAYLOCK:
        try:
            gateway = _GATEWAYS[idx]
            return (0, gateway.set_params(params))
        except Exception as e:
            return (-1, str(e))

# =====

def get_html(idx: int) -> tuple:
    """ TODO """
    with _GATEWAYLOCK:
        try:
            gateway = _GATEWAYS[idx]
            return (0, gateway.get_html())
        except Exception as e:
            return (-1, str(e))

#######

class PluginGatewayBase():
    """ TODO """
    version = '1.0'

    def __init__(self, module):
        self.module = module
        self.param = {}
        self.timer_next = None
        self.timer_period = None

    def init(self):
        """ init a new instance after adding to task list or reinit an existing instance after loading/changing params """
        if not self.timer_next and self.timer_period and self.get_params('enable'):
            self.timer_next = Timer.clock() + self.timer_period

    def exit(self):
        """ exit an existing instance after removing from task list """
        pass

    def get_name(self) -> str:
        """ get the name from the module """
        return self.param.get('name', 'Unknown')

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
        #self.param.update(param_new)
        changed = False
        for key in self.param:
            if self.param[key] != param_new.get(key, None):
                changed = True
                break

        if changed:
            self.exit()
            for key in self.param:
                self.param[key] = param_new.get(key, None)
            self.init()

    def get_html(self) -> str:
        """ get the html template name from the module """
        return 'web/www/gateways/{}.html'.format(self.module.GWPID)

    def cmd(self, cmd: str) -> str:
        return None

    def timer(self):
        pass

    def variables(self, news:dict):
        pass

#######
