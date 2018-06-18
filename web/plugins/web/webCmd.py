"""
Web Plugin for Command-Test-Page
"""
from com.Globals import *

from web.MicroWebSrv.microWebSrv import MicroWebSrv

import com.Tool as Tool
import web.Web as Web

#######

@MicroWebSrv.route('/cmd')
@MicroWebSrv.route('/cmd', 'POST')
def web_cmd(httpClient, httpResponse):
    """ Shows a form to enter a command and display the result for testing the ezPiC-commands """
    cmd = ''
    err = ''
    ret = ''
    formParams = None

    if httpClient.GetRequestMethod() == 'POST':
        formParams = httpClient.ReadRequestPostedFormData()
    else: # GET
        formParams  = httpClient.GetRequestQueryParams()

    if formParams and 'cmd' in formParams:
        cmd = formParams.get('cmd')
        #cmd = html.escape(cmd)

    if cmd:
        err, ret = Web.command(httpResponse, cmd, useCLI=True, source=httpClient._addr)
        ret = Tool.json_str(ret)
        #ret = html.escape(ret)
        log(LOG_DEBUG, 'Web command: {}', cmd)

    vars = {}
    vars['menu'] = 'tools'
    vars['cmd'] = cmd
    vars['err'] = err
    vars['ret'] = ret

    return httpResponse.WriteResponsePyHTMLFile('web/www/cmd.html', vars=vars)

#######
