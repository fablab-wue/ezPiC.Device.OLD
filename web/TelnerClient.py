"""
...TODO
"""
from com.Globals import *

import telnetlib

import com.Tool as Tool

#######
# Globals:

#PLUGINDIR = 'web/plugins/web'
TIMEOUT = 3
TEL = None
HOST = 'localhost'
PORT = 10123

#######

def excecute(request:str) -> str:
    global TEL, TIMEOUT, HOST, PORT

    if not TEL:
        TEL = telnetlib.Telnet(HOST, port=PORT, timeout=TIMEOUT)
        if not TEL:
            return '[-2301, "No corrention possible to {}"]'.format(HOST)
        #wait init sequence
    
    #empty stream

    #send request

    #readline answer

    return '[-2399, "Not implemented"]'

"""
import telnetlib
import time
import sys
import msvcrt


__author__ = "Rob Braggaar"
__license__ = "CC-BY-SA"

sys.ps1 = ''
sys.ps2 = ''
# timeout value for blocking operations [s]
TO = 5 

# host, 192.168.4.1 by default
host = "192.168.4.1"

# username and password for telnet
username = "micro"
password = "python"

# create telnet object
tel = telnetlib.Telnet(host, port=23, timeout=TO)

# login process
print tel.read_until("Login as: ")
print username
tel.write(username + "\r\n")
print tel.read_until("Password: ", timeout=TO)
print ''
time.sleep(1)
tel.write(password + "\r\n")
time.sleep(.5)
print tel.read_until(">>> ", timeout=TO).strip('>>> ')

# receive commands from the user as input
# send and execute commands to the pycom device and return the result
while True:
    indent = '    '
    cmd = raw_input('>>> ')
    if len(cmd) > 1:
        while cmd[-1] == ':':
            cmd += '\n' + indent + raw_input('... ' + indent)
            indent += '    '
    tel.write(cmd + '\r\n')
    time.sleep(.5)
    print (tel.read_until(">>> ", timeout=1).strip('>>> ' + cmd).strip('\r\n'))


"""