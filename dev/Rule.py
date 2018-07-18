"""
...TODO
"""
from com.Globals import *

import com.Tool as Tool
import dev.Timer as Timer

#######
# Globals:

_PLUGINDIR = 'dev/plugins/rules'
_RULEPLUGINS = {}
_RULES = []
_RULELOCK = RLock()
_RULETIMER = 0

#######

def rule_timer_handler(news, args):
    global _RULES, _RULETIMER

    with _RULELOCK:
        t = Timer.clock()

        for idx, rule in enumerate(_RULES):
            if rule.timer_next and (t >= rule.timer_next):
                if rule.get_params('ENABLE'):
                    if rule.timer_period:   # cyclic timer
                        rule.timer_next += rule.timer_period
                        if rule.timer_next < t:   # missed some events
                            rule.timer_next = t + rule.timer_period
                    else:   # singel event
                        rule.timer_next = None
                    rule.timer()
                else:   # disabled
                    rule.timer_next = None

            if news:
                if rule.get_params('ENABLE'):
                    rule.variables(news)

#######

def init():
    """ Prepare module vars and load plugins """
    global _RULEPLUGINS

    plugins = Tool.load_plugins(_PLUGINDIR, 'ru')
    for plugin in plugins:
        try:
            _RULEPLUGINS[plugin.EZPID] = plugin
        except:
            pass

# =====

def run():
    """ TODO """
    global _RULEPLUGINS, _RULETIMER

    Timer.register_cyclic_handler(rule_timer_handler)

#######

def load(config_all: dict):
    if not "rules" in config_all:
        return
    for config in config_all["rules"]:
        try:
            ezPID = config["EZPID"]
            loaded_version = config["version"]
            params = config["params"]
            err, idx = add(ezPID, params)
            running_version = _RULES[idx].version

            if not err and loaded_version != running_version:
                log(LOG_WARN, "task " +  ezPID + " has change version form " + loaded_version + " to " + running_version)
        except Exception as e:
            pass

# =====

def save(append: dict = None):
    ret = []
    with _RULELOCK:
        for rule in _RULES:
            try:
                config = {}
                config["EZPID"] = rule.module.EZPID
                config["version"] = rule.version
                config["params"] = rule.get_params()
                ret.append(config)
            except Exception as e:
                return (-1, str(e))

    if not append is None:
        append["rules"] = ret
        return (0, append)
    
    return (0, {"rules": ret})

#######

def add(plugin_id: str, params: dict = None) -> tuple:
    """ TODO """
    with _RULELOCK:
        try:
            module = _RULEPLUGINS.get(plugin_id, None)
            if module:
                rule = module.PluginRule(module)
                _RULES.append(rule)
                ret = len(_RULES) - 1
                if params:
                    rule.set_params(params)
                return (0, ret)
            else:
                return (-1, 'Unknown EZPID')
        except Exception as e:
            return (-1, str(e))


# =====

def delete(idx: int) -> tuple:
    """ TODO """
    with _RULELOCK:
        try:
            rule = _RULES[idx]
            rule.exit()
            del _RULES[idx]
            return (0, None)
        except Exception as e:
            return (-1, str(e))


# =====

def clear() -> tuple:
    """ TODO """
    global _RULES

    with _RULELOCK:
        for rule in _RULES:
            try:
                rule.exit()
            except Exception as e:
                return (-1, str(e))
        _RULES = []

    return (0, None)

# =====

def get_plugin_list() -> tuple:
    """ TODO """
    pl = []

    with _RULELOCK:
        for ezPID, module in _RULEPLUGINS.items():
            p = {}
            p['EZPID'] = module.EZPID
            p['PNAME'] = module.PNAME
            p['PINFO'] = module.PINFO
            p['PFILE'] = module.__name__
            pl.append(p)

    return (0, pl)

# =====

def get_list() -> tuple:
    """ TODO """
    gl = []

    with _RULELOCK:
        for idx, rule in enumerate(_RULES):
            g = {}
            g['idx'] = idx
            g['EZPID'] = rule.module.EZPID
            g['PNAME'] = rule.module.PNAME
            g['NAME'] = rule.get_name()
            g['ENABLE'] = rule.get_params('ENABLE')
            g['info'] = rule.get_info()
            gl.append(g)

    return (0, gl)

# =====

def get_params(idx: int, key: str=None) -> tuple:
    """ TODO """
    with _RULELOCK:
        try:
            rule = _RULES[idx]
            return (0, rule.get_params(key))
        except Exception as e:
            return (-1, str(e))


# =====

def set_params(idx: int, params: dict) -> tuple:
    """ TODO """
    with _RULELOCK:
        try:
            rule = _RULES[idx]
            return (0, rule.set_params(params))
        except Exception as e:
            return (-1, str(e))

# =====

def get_html(idx: int) -> tuple:
    """ TODO """
    with _RULELOCK:
        try:
            rule = _RULES[idx]
            return (0, rule.get_html())
        except Exception as e:
            return (-1, str(e))

#######

class PluginRuleBase():
    """ TODO """
    version = '1.0'

    def __init__(self, module):
        self.module = module
        self.param = {}
        self.timer_next = 0
        self.timer_period = 0

    def init(self):
        """ init a new instance after adding to task list or reinit an existing instance after loading/changing params """
        if not self.timer_next and self.timer_period and self.get_params('ENABLE'):
            self.timer_next = Timer.clock() + self.timer_period

    def exit(self):
        """ exit an existing instance after removing from task list """
        pass

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
                if self.param.get('ENABLE', False):
                    self.init()
                break

    def get_html(self) -> str:
        """ get the html template name from the module """
        return 'web/www/rules/{}.html'.format(self.module.EZPID)

    def cmd(self, cmd: str) -> str:
        return None

    def timer(self):
        pass

    def variables(self, news:dict):
        pass

#######
