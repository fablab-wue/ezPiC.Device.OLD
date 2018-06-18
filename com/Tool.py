"""
Common tools
"""
from com.Globals import *

import gc

#######

LOGO = '''\r\n\
                       _|_|_|    _|     _|_|_|\r\n\
    _|_|    _|_|_|_|   _|    _|       _|\r\n\
  _|    _|        _|   _|    _|  _|   _|\r\n\
  _|_|_|_|      _|     _|_|_|    _|   _|\r\n\
  _|          _|       _|        _|   _|\r\n\
    _|_|_|  _|_|_|_|   _|        _|     _|_|_|\r\n\
 \r\n\
 ezPiC IoT-Device - github.com/fablab-wue/ezPiC.Device\r\n\r\n'''

#######

def load_plugins(path: str, pre :str=None) -> list:
    """
    Imports all python modules from given path inside the plugin folder
    path: Relative path name
    pre: (optional) Filter python files/modules with start string
    return: List of imported modules
    """
    gc.collect()

    try:
        full_path = os.path.join(os.path.dirname(__file__), '..', path)
    except:   # MicroPython has no os.path
        full_path = '../' + path
    log(LOG_DEBUG, 'Loading plugins from path "{}"', full_path)

    modules = []

    files = []
    try:
        files = os.listdir(full_path)
    except:   # Micropython on Windows/Linux or path does not exist
        try:
            for f in os.ilistdir(full_path):
                files.append(f[0])
        except:
            pass
    log(LOG_EXT_DEBUG, ' - Plugin files: {}', files)

    module_prefix = path.replace('/', '.')

    gc.collect()

    for file in files:
        if file.startswith('__'):
            continue
        if not file.endswith('.py'):
            continue
        if pre and not file.startswith(pre):
            continue
        
        module_name = module_prefix + '.' + file[:-3]
        try:
            gc.collect()
            #log(LOG_DEBUG, 'MEM "{}"'.format(gc.mem_free()))
            module = __import__(module_name, globals(), locals(), ['object'], 0)
            gc.collect()
            modules.append(module)
            gc.collect()
            #log(LOG_DEBUG, 'MEM "{}"'.format(gc.mem_free()))
            log(LOG_DEBUG, ' - Import plugin "{}"', module_name)
        except Exception as e:
            gc.collect()
            #log(LOG_DEBUG, 'MEM "{}"'.format(gc.mem_free()))
            log(LOG_DEBUG, ' - Fail to import plugin "{}"\n{}', module_name, e)

    gc.collect()
    return modules

#######

def params_to_str(params:dict) -> str:
    """ converts the param dict to a string """

    return json.dumps(params)

# =====

def str_to_params(paramstr:str) -> dict:
    """ converts the string to a param dict """

    return json.loads(paramstr)

#######

def start_thread(func, *args):
    gc.collect()

    #if MICROPYTHON:
    if True:
        from _thread import start_new_thread

        t = start_new_thread(func, ())
        return t
    else:
        from threading import Thread

        t = Thread(name=func.__name__, target=func, args=args)
        t.setDaemon(True)
        t.start()
        return t

#######

def load_cnf():
    CNF['logLevel']   = LOG_EXT_DEBUG
    CNF['logFile']    = None

    CNF['useIoT']     = True
    CNF['useWeb']     = not MICROPYTHON
    CNF['useCLI']     = True
    CNF['useTelnet']  = False

    CNF['portWeb']    = 10180
    CNF['portTelnet'] = 10123

    try:
        with open('ezPiC.cnf', 'r') as infile:
            cnf = json.load(infile)
            CNF.update(cnf)
    except:
        pass

#######

def json_str(o):
    try:
        if MICROPYTHON:
            return json.dumps(o)
        else:
            return json.dumps(o, indent=2)
    except:
        return str(o)

#######