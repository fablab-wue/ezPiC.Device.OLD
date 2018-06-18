"""
...TODO
"""

from com.Globals import *

from argparse import ArgumentParser

parser = ArgumentParser(prog='ezPiC', conflict_handler='resolve')

parser.add_argument("-w", "--noweb",
                    dest="useWeb", default=CNF['useWeb'], action="store_false", 
                    help="Don't start web server part")
parser.add_argument("-W", "--useweb",
                    dest="useWeb", default=CNF['useWeb'], action="store_true", 
                    help="Start web server part")
                    
parser.add_argument("-i", "--noiot",
                    dest="useIoT", default=CNF['useIoT'], action="store_false", 
                    help="Don't start IoT part")
parser.add_argument("-I", "--useiot",
                    dest="useIoT", default=CNF['useIoT'], action="store_true", 
                    help="Start IoT part")
                    
parser.add_argument("-c", "--nocli",
                    dest="useCLI", default=CNF['useCLI'], action="store_false", 
                    help="Don't allow CLI commands")
parser.add_argument("-C", "--usecli",
                    dest="useCLI", default=CNF['useCLI'], action="store_true", 
                    help="Allow CLI commands")

parser.add_argument("-t", "--notelnet",
                    dest="useTelnet", default=CNF['useTelnet'], action="store_false", 
                    help="Don't allow Telnet commands")
parser.add_argument("-T", "--usetelnet",
                    dest="useTelnet", default=CNF['useTelnet'], action="store_true", 
                    help="Allow Telnet commands")

parser.add_argument("-l", "--loglevel", 
                    dest="logLevel", default=CNF['logLevel'], type=int, metavar="LEVEL",
                    help="Set the maximum logging level - 0=no output, 1=error, 2=warning, 3=info, 4=debug, 5=ext.debug")

parser.add_argument("-L", "--logfile", 
                    dest="logFile", default=CNF['logFile'], metavar="FILE",
                    help="Set FILE name for logging output")

parser.add_argument("-p", "--porttelnet", 
                    dest="portTelnet", default=CNF['portTelnet'], metavar='PORT', type=int,
                    help="Set the TCP port for telnet server")

parser.add_argument("-P", "--portweb", 
                    dest="portWeb", default=CNF['portWeb'], metavar='PORT', type=int,
                    help="Set the TCP port for web server")

parser.add_argument("-s", "--savecnf",
                    dest="saveCnf", default=False, action="store_true", 
                    help="Save actual configuration to file 'ezPiC.cnf'")

# TESTING
parser.add_argument("-q", "--quiet",
                    dest="verbose", default=True, action="store_false", 
                    help="don't print status messages to stdout")
parser.add_argument("-n", 
                    metavar='N', type=int,
                    help="print the N-th fibonacci number")
parser.add_argument("-x",
                    dest="x", default=10, type=int,
                    help="how many lines get printed")

args = parser.parse_args()

CNF['useWeb'] = args.useWeb
CNF['useIoT'] = args.useIoT
CNF['useCLI'] = args.useCLI
CNF['useTelnet'] = args.useTelnet
CNF['logLevel'] = args.logLevel
CNF['logFile'] = args.logFile
CNF['portTelnet'] = args.portTelnet
CNF['portWeb'] = args.portWeb

log(LOG_EXT_DEBUG, 'cnf: {}', CNF)

if args.saveCnf:
    with open('ezPiC.cnf', 'w') as f:
        json.dump(CNF, f, indent=0)
    
#######

