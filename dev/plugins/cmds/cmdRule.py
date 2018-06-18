"""
Command Plugin for handling Rules
"""
from com.Globals import *

import dev.Rule as Rule
import dev.Cmd as Cmd

#######

@Cmd.route('plugin.rule.list')
@Cmd.route('prul')
def cmd_rule_list(cmd:dict) -> tuple:
    """ gets a list of all available RULE plugins """
    err, ret = Rule.get_plugin_list()

    return (err, ret)

#######

@Cmd.route('rule.list')
@Cmd.route('rul')
def cmd_rule_task_list(cmd:dict) -> tuple:
    """ gets a list of all RULE instances """
    err, ret = Rule.get_list()

    return (err, ret)

#######

@Cmd.route('rule.add', 'rupid')
def cmd_rule_add(cmd:dict) -> tuple:
    """ adds a new instance of a RULE plugin """
    err, ret = Rule.add(cmd.get('rupid', None))

    return (err, ret)

#######

@Cmd.route('rule.clear')
@Cmd.route('rule.del.all')
def cmd_rule_del_all(cmd:dict) -> tuple:
    """ remove all RULE instances """
    err, ret = Rule.clear()

    return (err, ret)

#######

@Cmd.route('rule.del.#')
def cmd_rule_del(cmd:dict) -> tuple:
    """ remove one RULE instance """
    index = cmd['IDX']
    err, ret = Rule.delete(index)

    return (err, ret)

#######

@Cmd.route('rule.getparams.#', 'key')
def cmd_rule_get(cmd:dict) -> tuple:
    """ gets params from one RULE instance """
    index = cmd['IDX']
    key = cmd.get('key', None)
    err, ret = Rule.get_params(index, key)

    return (err, ret)

#######

@Cmd.route('rule.setparams.#', 'params')
def cmd_rule_set(cmd:dict) -> tuple:
    """ sets params for one RULE instance """
    index = cmd['IDX']
    params = cmd.get('params', None)
    if params and type(params) is str:
        params = json.loads(params)
    err, ret = Rule.set_params(index, params)

    return (err, ret)

#######

@Cmd.route('rule.gethtml.#')
def cmd_rule_html(cmd:dict) -> tuple:
    """ gets the correcponding html page name for the RULE instance/plugin """
    index = cmd['IDX']
    err, ret = Rule.get_html(index)

    return (err, ret)

#######
