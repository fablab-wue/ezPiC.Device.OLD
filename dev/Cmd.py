"""
...TODO
"""
from com.Globals import *

import com.Tool as Tool

#######
# Globals:

PLUGINDIR = 'dev/plugins/cmds'
COMMANDS = []

#######
#Decorator

def route(command:str, arg_keys:str=None, security_level:int=0, menu:str=None, html:str=None, text:str=None):
    """ Adds a command handler function to the command list """
    def route_decorator(func):
        global COMMANDS

        item = {}
        if command.endswith('.#'):
            item['command'] = command[:-2]
            item['has_index'] = True
        else:
            item['command'] = command
            item['has_index'] = False

        if arg_keys:
            item['args'] = arg_keys.split()
        else:
            item['args'] = None

        item['func'] = func

        COMMANDS.append(item)
        log(LOG_EXT_DEBUG, '    - Added command "{}" with function "{}()"', command, func.__name__)
        return func

    return route_decorator

#######

def _split_ex(src_str:str) -> list:
    #return src_str.split(' ')
    ret = []
    line = src_str.strip()

    while line:
        c = line[0]
        if c == '"':
            parts = line[1:].split('"')   # find end of string
            ret.append(parts[0])
            if len(parts) <= 1:   # if end of line reached all done
                return ret
            line = parts[1].strip()
            continue

        if c == '{' or c == '[':   # is possible JSON string?
            # First: check if hole line is a JSON string
            try:
                _ = json.loads(line)
                ret.append(line)   # survived! A valid JSON string!
                return ret
            except:
                pass   # no JSON string
            # Hack: Second: try every line length to find a valid JSON string - feel free to fing a better solution!
            i = 2
            while i < len(line):
                try:
                    _ = json.loads(line[:i])
                    ret.append(line[:i])   # survived! A valid JSON string!
                    line = line[i:].strip()   # continue with rest line
                    i = -1
                    break
                except:
                    pass   # no JSON string - so far...
                i += 1
            if i < 0:   # Hack to continue over 2 while
                continue

        # no specials - split on spaces
        parts = line.split(' ', 1)
        ret.append(parts[0])
        if len(parts) <= 1:
            return ret
        line = parts[1]   # continue with rest line
        continue

    return ret

#######

def init():
    """ Prepare module vars and load plugins """
    global COMMANDS

    plugins = Tool.load_plugins(PLUGINDIR, 'cmd')

# =====

def run():
    pass

#######

def _excecute_line(cmd_str: str, source=None) -> tuple:
    """
    Excecutes a command as str
    cmd: Command line with command and params as string
    return: Answer from excecuted command. Can be any object type or None
    """
    for c in COMMANDS:
        if cmd_str.startswith(c['command']):   # command found
            cmd_params = {}

            cmd_arg = cmd_str.split(' ', 1)
            cmd = cmd_arg[0]
            cmd_params['CMD'] = cmd

            if c['has_index']:
                l = len(c['command'])
                index_str = cmd[l+1:]
                if index_str:
                    cmd_params['IDX'] = int(index_str)
                else:
                    return (-903, 'Command needs index')

            if c['args'] and len(cmd_arg)>1:
                arg_str = cmd_arg[1].strip()
                #TODO check json
                args = _split_ex(arg_str)
                i = 0
                for key in c['args']:
                    if i<len(args):
                        value = args[i]
                        cmd_params[key] = value
                    else:
                        cmd_params[key] = None
                    i += 1

            cmd_params['SRC'] = source
                
            fHandler = c['func']

            try:
                return fHandler(cmd=cmd_params)
            except Exception as e:
                return (-901, 'Exception in command handler - ' + str(e))

    return (-900, 'Unknown command: "' + cmd_str + '"')

# =====

def _excecute_json(cmd_dict: dict, source=None) -> tuple:
    """
    Excecutes a command as a dict
    cmd: Command dict with dict-items as params
    return: Answer from excecuted command. Can be any object type or None
    """
    cmd_params = cmd_dict

    cmd_str = cmd_params.get('CMD', None)
    if not cmd_str:
        return (-911, 'JSON-Command has no item "CMD"')
    
    for c in COMMANDS:
        if cmd_str == c['command']:   # command found

            if c['has_index']:
                index = cmd_params.get('IDX', None)
                if index is None:
                    return (-903, 'Command needs index')

            if source:
                cmd_params['SRC'] = source
                
            fHandler = c['func']

            try:
                return fHandler(cmd=cmd_params)
            except Exception as e:
                return (-901, 'Exception in command handler - ' + str(e))

    return (-900, 'Unknown command: ' + cmd_str)

# =====

def excecute(cmd, source=None) -> tuple:
    """
    Excecutes a command and route to specified handler
    cmd: Command as str or JSON-str or dict
    return: Answer from excecuted command. Can be any object type or None
    """
    try:
        if type(cmd) is str:
            cmd = cmd.strip()
            if cmd.startswith('{') and cmd.endswith('}'):
                cmd_dict = json.loads(cmd)
                return _excecute_json(cmd_dict, source)
            else:
                return _excecute_line(cmd, source)
        elif type(cmd) is dict:
            return _excecute_json(cmd, source)
        else:
            return (-909, 'Wrong type in command parser: ' + str(type(cmd)))
        
    except Exception as e:
        return (-902, 'Exception in command parser - ' + str(e))

    return (-999, 'Error')

#######