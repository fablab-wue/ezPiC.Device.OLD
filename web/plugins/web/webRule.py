"""
Web Plugin for Rule-Pages
"""
from com.Globals import *

from web.MicroWebSrv.microWebSrv import MicroWebSrv

import com.Tool as Tool
import web.Web as Web

#######

@MicroWebSrv.route('/rules')
def web_rules(httpClient, httpResponse):
    """ TODO """

    err, ret = Web.command(httpResponse, 'rule.list')
    if err:
        Web.flash_error(httpResponse, err, ret)
        ret = []

    vars = {}
    vars['menu'] = 'rules'
    vars['rule_list'] = ret

    return httpResponse.WriteResponsePyHTMLFile('web/www/rules.html', vars=vars)

#######

@MicroWebSrv.route('/rules/stage/')
def web_rules_list(httpClient, httpResponse):
    """ TODO """

    err, ret = Web.command(httpResponse, 'rule.stage.list')
    if err:
        Web.flash_error(httpResponse, err, ret)
        ret = []

    vars = {}
    vars['menu'] = 'rules'
    vars['rule_list'] = ret

    return httpResponse.WriteResponsePyHTMLFile('web/www/rules_list.html', vars=vars)

#######

@MicroWebSrv.route('/rules/add/<ezPID>/')
def web_rule_add(httpClient, httpResponse, args):
    """ TODO """
    ezPID = args['ezPID']

    params = {'ezPID': ezPID}
    err, ret = Web.command(httpResponse, 'rule.add', items=params)
    if err:
        Web.flash_error(httpResponse, err, ret, ezPID)
    else:
        Web.command(httpResponse, 'save')
        msg = 'Rule "{}" added'.format(ezPID)
        httpResponse.FlashMessage(msg, 'info')

    return httpResponse.WriteResponseRedirect('/rules')

#######

@MicroWebSrv.route('/rules/edit/<idx>/')
@MicroWebSrv.route('/rules/edit/<idx>/', 'POST')
def web_rule_edit(httpClient, httpResponse, args):
    """ TODO """
    idx = int(args['idx'])

    err, ret = Web.command(httpResponse, 'rule.getparams', index=idx)
    if err:
        Web.flash_error(httpResponse, err, ret, idx)
        return httpResponse.WriteResponseRedirect('/rules')

    params = {}
    params.update(ret)

    if httpClient.GetRequestMethod() == 'POST':
        formParams = httpClient.ReadRequestPostedFormData()        
        if formParams:
            formParams['ENABLE'] = 'ENABLE' in formParams   # checkbox -> bool
            params.update(formParams)
        err, ret = Web.command(httpResponse, 'rule.setparams', index=idx, params=formParams)
        if not err:
            err, ret = Web.command(httpResponse, 'save')
        if err:
            Web.flash_error(httpResponse, err, ret, idx)
        else:
            httpResponse.FlashMessage('Settings saved', 'info')
    else: # GET
        pass

    vars = {}
    vars['menu'] = 'rules'
    vars['index'] = idx
    vars.update(params)

    err, html = Web.command(httpResponse, 'rule.gethtml', index=idx)

    return httpResponse.WriteResponsePyHTMLFile(html, vars=vars)

#######

@MicroWebSrv.route('/rules/del/<idx>/')
def web_rule_del(httpClient, httpResponse, args):
    """ TODO """
    idx = int(args['idx'])

    err, ret = Web.command(httpResponse, 'rule.delete', index=idx)
    if err:
        Web.flash_error(httpResponse, err, ret, idx)
    else:
        err, ret = Web.command(httpResponse, 'save')
        msg = 'Rule instance deleted'
        httpResponse.FlashMessage(msg, 'info')

    return httpResponse.WriteResponseRedirect('/rules')

#######
