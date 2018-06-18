"""
...TODO
"""
from com.Globals import *

import serial

import com.Tool as Tool

#######
# Globals:

SER = None
SER_PORT = 'socket://localhost:10123'

#######

def open():
    global SER, SER_PORT

    if SER and SER.is_open:
        return (0, 'Already Open')

    try:
        SER = serial.serial_for_url(SER_PORT, do_not_open=True)
        SER.baudrate = 115200
        SER.inter_byte_timeout = 0.01
        SER.timeout = 2.5
        SER.open()

        if not SER.is_open:
            return (-601, 'Remote Port connected but not open')

        #SER.reset_in_buffer()

        for n in range(3):
            SER.write(b'\r\n')
            time.sleep(0.2)
            while SER.in_waiting:
                c = SER.read(SER.in_waiting)

    except Exception as e:
        SER = None
        log(LOG_DEBUG, 'Failed to open Remote Port: {} -> {}', SER_PORT, str(e))
        return (-600, str(e))

    log(LOG_DEBUG, 'Open Remote Port: {}', SER_PORT)
    return (0, 'Open')


def close():
    global SER, SER_PORT

    if SER:
        SER.close()
    SER = None

    return (0, None)


def is_open():
    global SER, SER_PORT

    if not SER:
        return False
    return SER.is_open


def set_port(ser_port:str):
    global SER, SER_PORT

    if SER_PORT != ser_port:
        close()
    SER_PORT = ser_port
    log(LOG_DEBUG, 'Set new Remote Port: {}', SER_PORT)


def get_port():
    global SER, SER_PORT

    return SER_PORT


def excecute(cmd:str, source=None) -> tuple:
    ret_b = bytearray()

    try:
        if not is_open():
            open()

        if SER.in_waiting:
            #SER.reset_in_buffer()
            while SER.in_waiting:
                c = SER.read(SER.in_waiting)

        cmd_b = cmd.encode('utf-8')
        SER.write(cmd_b)
        SER.write(b'\r\n')

        for n in range(3):
            c = SER.read()   # blocking with 1 byte
            ret_b.extend(c)

            while SER.in_waiting:
                c = SER.read(SER.in_waiting)
                ret_b.extend(c)

            i = ret_b.find(b'\r\n\r\n')
            if i >= 0:
                break

        ret = ret_b.decode('utf-8')
        ret = ret.strip()

        # cut all after JSON end
        i = ret.find('\r\n\r\n')
        if i >= 0:
            ret = ret[:i]

        # cut local echo
        if ret.startswith(cmd):
            ret = ret[len(cmd):]

        ret = ret.replace('\r\n', ' ')
        ret = ret.strip()

        return (0, ret)
        #return '[-2399, "Not implemented"]'

    except Exception as e:
        return (-601, str(e))

def get_com_ports():
    ports = []
    try:
        from serial.tools.list_ports import comports
        for n, (port_id, port_desc, hwid) in enumerate(sorted(comports()), 1):
            #port_str = port_id + ' - ' + port_desc + ' [' + hwid + ']'
            #ports.append(port_str)
            ports.append((port_id, port_desc, hwid))
    except:
        pass

    return(ports)