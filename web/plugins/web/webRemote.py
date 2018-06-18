"""
Web Plugin for Remote-Setup-Page
"""
from com.Globals import *

from web.MicroWebSrv.microWebSrv import MicroWebSrv

import com.Tool as Tool
import web.Web as Web
import web.Remote as Remote

#######

@MicroWebSrv.route('/remote')
@MicroWebSrv.route('/remote', 'POST')
def web_remote(httpClient, httpResponse):
    """ Shows a form to enter the COM port or IP Address of a alien ezPiC-Board """
    status = 'Not connected'
    formParams = None

    port = Remote.get_port()

    if httpClient.GetRequestMethod() == 'POST':
        formParams = httpClient.ReadRequestPostedFormData()
    else: # GET
        formParams  = httpClient.GetRequestQueryParams()

    if formParams and 'port' in formParams:
        port = formParams.get('port')

    if port:
        Remote.set_port(port)
        err, ret = Remote.open()
        if err:
            Web.flash_error(httpResponse, err, ret)
        status = ret

    vars = {}
    vars['menu'] = 'remote'
    vars['port'] = port
    vars['status'] = status
    vars['com_ports'] = Remote.get_com_ports()

    return httpResponse.WriteResponsePyHTMLFile('web/www/remote.html', vars=vars)

#######

@MicroWebSrv.route('/remote/close')
def web_remote_close(httpClient, httpResponse):
    """ Shows a the remote page after closing the remote port """
    Remote.close()

    vars = {}
    vars['menu'] = 'remote'
    vars['port'] = ''
    vars['status'] = 'CLOSED'
    vars['com_ports'] = Remote.get_com_ports()

    return httpResponse.WriteResponsePyHTMLFile('web/www/remote.html', vars=vars)

#######
