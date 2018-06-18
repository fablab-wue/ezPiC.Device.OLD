#!/usr/bin/env python3
"""
ezPiC - IoT-Device
"""
# Meta
__version__ = '0.0.1'
__version_info__ = (0, 0, 1)
__author__ = 'Jochen Krapf et al.'
__license__ = "GNU General Public License (GPL) Version 3"

#import test

from com.Globals import *

# get program configuration
import com.Tool as Tool
Tool.load_cnf()
try:   # CPython only
    import com.Args
except Exception as e:
    pass
LOG_LEVEL = CNF['logLevel']


# load module dependent on configuration
if CNF['useWeb']:
    try:
        import web.Web as Web
    except Exception as e:
        log(LOG_ERROR, str(e))
        CNF['useWeb'] = False
if CNF['useIoT']:
    try:
        import dev.Cmd as Cmd
        import dev.Timer as Timer
        import dev.Machine as Machine
        import dev.Gadget as Gadget
        import dev.Gateway as Gateway
        import dev.Rule as Rule
        import dev.Device as Device
        import dev.Variable as Variable
        if CNF['useCLI']:
            try:
                import dev.CLI as CLI
            except Exception as e:
                log(LOG_ERROR, str(e))
                CNF['useCLI'] = False
        if CNF['useTelnet']:
            try:
                import dev.TelnetServer as TelnetServer
            except Exception as e:
                log(LOG_ERROR, str(e))
                CNF['useTelnet'] = False
    except Exception as e:
        log(LOG_ERROR, str(e))
        CNF['useIoT'] = False

#######

def main():
    """ Entry point for ezPiC """
    #test.main()

    log(LOG_DEBUG, '# Starting main init')
    if CNF['useIoT']:
        Timer.init()
        Cmd.init()
        Machine.init()
        Gadget.init()
        Gateway.init()
        Rule.init()
        Device.init()
        Variable.init()
        if CNF['useCLI']:
            CLI.init()
        if CNF['useTelnet']:
            TelnetServer.init(port=CNF['portTelnet'])
    if CNF['useWeb']:
        Web.init(port=CNF['portWeb'])

    log(LOG_INFO, '# Starting main run')
    if CNF['useIoT']:
        Timer.run()
        Cmd.run()
        Machine.run()
        Gadget.run()
        Gateway.run()
        Rule.run()
        Device.run()
        Variable.run()

        # DEBUG
        if not MICROPYTHON:
            Cmd.excecute('vs Lorem_ {"e": 2, "d": 756, "c": 234, "b": 12313, "a": 123}')
            Cmd.excecute('vs Lörém_ [0, 8, 15]')
            Cmd.excecute('vs Lorem {"e":2,"d":756,"c":234,"b":12313,"a":123}')
            Cmd.excecute('vs Lörém [0,8,15]')

        log(LOG_DEBUG, '# Load settings')
        Cmd.excecute("load")

    if CNF['useWeb']:
        log(LOG_DEBUG, '# Starting web server')
        Web.run(threaded=CNF['useIoT'])   # this call never comes back .. normally

    if CNF['useIoT']:
        if CNF['useCLI']:
            log(LOG_DEBUG, '# Starting CLI')
            CLI.run(threaded=CNF['useTelnet'])
        if CNF['useTelnet']:
            log(LOG_DEBUG, '# Starting telnet server')
            TelnetServer.run()   # this call never comes back .. normally

    log(LOG_ERROR, 'PANIC! Server terminated')
    RUN = False

#######

def __exit__():
    RUN = False
    log(LOG_ERROR, '<<<<<<<<EXIT>>>>>>>>>')

#######

if MICROPYTHON:
    main()   # this call never comes back!
    RUN = False
else:
    if __name__ == '__main__':
        main()   # this call never comes back!
        RUN = False

#######

