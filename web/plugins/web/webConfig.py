"""
Web Plugin for System-Config-Page
"""
from com.Globals import *

from web.MicroWebSrv.microWebSrv import MicroWebSrv

import com.Tool as Tool
import web.Web as Web

#######

@MicroWebSrv.route('/config')
@MicroWebSrv.route('/config', 'POST')
def web_config(httpClient, httpResponse):
    """ TODO """

    vars = {}
    vars['menu'] = 'config'
    vars['xyz'] = 'XYZ'
    vars['abc'] = '12345'

    vars['NAME'] = 'Test-Name'
    vars['info'] = 'BlaBla'

    if httpClient.GetRequestMethod() == 'POST':
        formParams = httpClient.ReadRequestPostedFormData()
        if formParams:
            for key, value in vars.items():
                if key in formParams:
                    vars[key] = formParams.get(key)
    else: # GET
        pass

    return httpResponse.WriteResponsePyHTMLFile('web/www/config.html', vars=vars)

#######
