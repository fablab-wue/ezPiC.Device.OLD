"""
Web Plugin for Variable-Pages
"""
from com.Globals import *

from web.MicroWebSrv.microWebSrv import MicroWebSrv

import com.Tool as Tool
import web.Web as Web

#######

@MicroWebSrv.route('/variables/<tick>')
@MicroWebSrv.route('/variables')
@MicroWebSrv.route('/variables', 'POST')
def web_variable_list(httpClient, httpResponse, args=None):
    """ TODO """
    key = ''
    value = ''
    if args:
        act_tick = int(args.get('tick', 0))
    else:
        act_tick = 0

    if httpClient.GetRequestMethod() == 'POST':
        formParams = httpClient.ReadRequestPostedFormData()
    else: # GET
        formParams  = httpClient.GetRequestQueryParams()

    if formParams and 'key' in formParams:
        key = formParams.get('key')
        value = formParams.get('value')
        variable = {}
        variable['key'] = key
        variable['value'] = value
        #variable['source'] = 'WEB-SET'
        err, ret = Web.command(httpResponse, 'variable.set', items=variable)
        if err:
            Web.flash_error(httpResponse, err, ret)

    err, ret = Web.command(httpResponse, 'variable.list', index=act_tick)
    if err:
        Web.flash_error(httpResponse, err, ret)
        ret = {}

    vars = {}
    vars['menu'] = 'tools'
    vars['variable_list'] = ret['variables']
    vars['last_tick'] = ret['tick']
    vars['act_tick'] = act_tick
    vars['add_key'] = key
    vars['add_value'] = value

    return httpResponse.WriteResponsePyHTMLFile('web/www/variables.html', vars=vars)

#######

@MicroWebSrv.route('/variablesfull/<tick>')
@MicroWebSrv.route('/variablesfull')
@MicroWebSrv.route('/variablesfull', 'POST')
def web_variable_full_list(httpClient, httpResponse, args=None):
    """ TODO """
    key = ''
    value = ''
    if args:
        act_tick = int(args.get('tick', 0))
    else:
        act_tick = 0

    if httpClient.GetRequestMethod() == 'POST':
        formParams = httpClient.ReadRequestPostedFormData()
    else: # GET
        formParams  = httpClient.GetRequestQueryParams()

    if formParams and 'key' in formParams:
        key = formParams.get('key')
        value = formParams.get('value')
        variable = {}
        variable['key'] = key
        variable['value'] = value
        #variable['source'] = 'WEB-SET'
        err, ret = Web.command(httpResponse, 'variable.set', items=variable)
        if err:
            Web.flash_error(httpResponse, err, ret)

    err, ret = Web.command(httpResponse, 'variable.full.list', index=act_tick)
    if err:
        Web.flash_error(httpResponse, err, ret)
        ret = {}

    vars = {}
    vars['menu'] = 'tools'
    vars['variable_list'] = ret['variables']
    vars['last_tick'] = ret['tick']
    vars['act_tick'] = act_tick
    vars['add_key'] = key
    vars['add_value'] = value

    return httpResponse.WriteResponsePyHTMLFile('web/www/variablesfull.html', vars=vars)

#######