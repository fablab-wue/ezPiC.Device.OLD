"""
...TODO
"""
from com.Globals import *

from .MicroWebSrv.microWebSrv import MicroWebSrv

import com.Tool as Tool
import web.Remote as Remote

# check if a direct call of commands are possible else use Telnet
try:
    import dev.Cmd as Cmd
    DIRECT_CMD = True
except:
    import TelnerClient
    DIRECT_CMD = False
    IOT_PART_ADDR = None


MWS = None
PORT = 80

#######
# Globals:

PLUGINDIR = 'web/plugins/web'

#######

def init(port):
    """ Prepare module vars and load plugins """
    global MWS, PORT

    PORT = port
    
    www = Tool.load_plugins(PLUGINDIR, 'web')

    MWS = MicroWebSrv(port=port, webPath='web/www') # TCP port 80 and files in /flash/www

# =====

def run(threaded=False):
    """ TODO """
    global MWS, PORT

    log (LOG_INFO, "Web server listen on port {}", PORT)

    MWS.Start(threaded=threaded)         # Starts server in a new thread

#######

def command(httpResponse, cmd_str:str, index:int=None, items:dict=None, params:dict=None, useCLI:bool=False, source:str=None) -> tuple:
    """ TODO """
    if useCLI:
        request = cmd_str
    else:
        request = {}
        request['CMD'] = cmd_str
        if index is not None:
            request['IDX'] = index
        if source:
            request['SRC'] = source
        else:
            request['SRC'] = 'WEB'
        if params is not None:
            request['params'] = params
        if items is not None:
            request.update(items)

    if Remote.is_open():
        request_json = json.dumps(request)
        err, answer_json = Remote.excecute(request_json)
        if err:
            return (err, answer_json)
        answer = json.loads(answer_json)

    elif DIRECT_CMD:
        answer = Cmd.excecute(request)
    else:
        request_json = json.dumps(request)
        answer_json = TelnerClient.excecute(request_json)
        answer = json.loads(answer_json)

    return tuple(answer)

#######

def flash_error(httpResponse, err, ret, idx=None):
    if idx:
        msg = 'Error {0} [{2}] - {1}'.format(err, ret, idx)
    else:
        msg = 'Error {0} - {1}'.format(err, ret)

    httpResponse.FlashMessage(msg, 'danger')

#######