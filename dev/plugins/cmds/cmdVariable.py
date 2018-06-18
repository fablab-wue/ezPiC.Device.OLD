"""
Command Plugin for handling Variables
"""
from com.Globals import *

import dev.Variable as Variable
import dev.Cmd as Cmd

#######

@Cmd.route('variable.full.list.#')
@Cmd.route('vfl.#')
def cmd_variable_full_list(cmd:dict) -> tuple:
    """ gets a list of dics with all variable parameters """
    index = cmd['IDX']
    last_tick, variables = Variable.get_news_full(index)
    ret = {'tick':last_tick, 'variables':variables}

    return (0, ret)

#######

@Cmd.route('variable.list.#')
@Cmd.route('vl.#')
def cmd_variable_list(cmd:dict) -> tuple:
    """ gets a list of dics with variable key and formatted value """
    index = cmd['IDX']
    last_tick, variables = Variable.get_news(index)
    ret = {'tick':last_tick, 'variables':variables}

    return (0, ret)

#######

@Cmd.route('variable.set', 'key value source')
@Cmd.route('vs', 'key value source')
def cmd_variable_set(cmd:dict) -> tuple:
    """ sets the value of a variable """
    key = cmd.get('key', None)
    value = cmd.get('value', None)
    source = cmd.get('SRC', None)
    source = cmd.get('source', source)
    
    try:
        if type(value) is str:
            value = json.loads(value)
    except:
        pass

    last_tick = Variable.set(key, value, source)
    
    return (0, last_tick)

#######
