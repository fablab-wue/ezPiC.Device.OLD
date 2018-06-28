"""
Command Line Interface for Configuration the IoT-Device
"""
from com.Globals import *

import com.Tool as Tool
import dev.Cmd as Cmd

#######
# Globals:

_PROMPT = ':-> '

#######

def thread_cli_loop(*argv):
    global _PROMPT

    time.sleep(0.75)
    print(Tool.LOGO)
    while RUN:
        cmd_str = input(_PROMPT)
        cmd_str = cmd_str.strip()
        if not cmd_str:
            continue
        err, ret = Cmd.excecute(cmd_str, 'CLI')
        if cmd_str.startswith('{'):   # cmd in JSON -> answer in JSON
            print(Tool.json_str([err, ret]))
        elif err is not None and err != 0:
            print( 'ERROR {}: {}'.format(err, ret) )
        elif ret:
            print(Tool.json_str(ret))
        print()

#######

def init():
    """ Prepare module vars and load plugins """
    pass

# =====

def run(threaded=True):
    if threaded:
        Tool.start_thread(thread_cli_loop, ())
    else:
        thread_cli_loop()   # this call never comes back .. normally
 
#######
