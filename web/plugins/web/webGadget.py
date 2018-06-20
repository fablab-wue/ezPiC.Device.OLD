"""
Web Plugin for Gadget-Pages
"""
from com.Globals import *

from web.MicroWebSrv.microWebSrv import MicroWebSrv

import com.Tool as Tool
import web.Web as Web

#######

@MicroWebSrv.route('/gadgets')
def web_gadgets(httpClient, httpResponse):
    """ TODO """

    err, ret = Web.command(httpResponse, 'gadget.list')
    if err:
        Web.flash_error(httpResponse, err, ret)
        ret = []

    vars = {}
    vars['menu'] = 'gadgets'
    vars['gadget_list'] = ret

    return httpResponse.WriteResponsePyHTMLFile('web/www/gadgets.html', vars=vars)

#######

@MicroWebSrv.route('/gadgets/list/')
def web_gadgets_list(httpClient, httpResponse):
    """ TODO """

    err, ret = Web.command(httpResponse, 'plugin.gadget.list')
    if err:
        Web.flash_error(httpResponse, err, ret)
        ret = []

    vars = {}
    vars['menu'] = 'gadgets'
    vars['gadget_list'] = ret

    return httpResponse.WriteResponsePyHTMLFile('web/www/gadgets_list.html', vars=vars)

#######

@MicroWebSrv.route('/gadgets/add/<gdpid>/')
def web_gadget_add(httpClient, httpResponse, args):
    """ TODO """
    gdpid = args['gdpid']

    params = {'gdpid': gdpid}
    err, ret = Web.command(httpResponse, 'gadget.add', items=params)
    if err:
        Web.flash_error(httpResponse, err, ret, gdpid)
    else:
        Web.command(httpResponse, 'save')
        msg = 'Gadget "{}" added'.format(gdpid)
        httpResponse.FlashMessage(msg, 'info')

    return httpResponse.WriteResponseRedirect('/gadgets')

#######

@MicroWebSrv.route('/gadgets/edit/<idx>/')
@MicroWebSrv.route('/gadgets/edit/<idx>/', 'POST')
def web_gadget_edit(httpClient, httpResponse, args):
    """ TODO """
    idx = int(args['idx'])

    err, ret = Web.command(httpResponse, 'gadget.getparams', index=idx)
    if err:
        Web.flash_error(httpResponse, err, ret, idx)
        return httpResponse.WriteResponseRedirect('/gadgets')

    params = {}
    params.update(ret)

    if httpClient.GetRequestMethod() == 'POST':
        formParams = httpClient.ReadRequestPostedFormData()        
        if formParams:
            formParams['ENABLE'] = 'ENABLE' in formParams   # checkbox -> bool
            formParams['timer'] = int(formParams.get('timer', 0))
            for key, value in params.items():
                if key in formParams:
                    params[key] = formParams.get(key)
        err, ret = Web.command(httpResponse, 'gadget.setparams', index=idx, params=params)
        if err:
            Web.flash_error(httpResponse, err, ret, idx)
        err, ret = Web.command(httpResponse, 'save')
        httpResponse.FlashMessage('Settings saved', 'info')
    else: # GET
        pass

    vars = {}
    vars['menu'] = 'gadgets'
    vars['index'] = idx
    vars.update(params)

    err, ret = Web.command(httpResponse, 'gadget.getfeatures', index=idx)
    if not err:
        vars.update(ret)

    err, html = Web.command(httpResponse, 'gadget.gethtml', index=idx)

    return httpResponse.WriteResponsePyHTMLFile(html, vars=vars)

#######

@MicroWebSrv.route('/gadgets/del/<idx>/')
def web_gadget_del(httpClient, httpResponse, args):
    """ TODO """
    idx = int(args['idx'])

    err, ret = Web.command(httpResponse, 'gadget.delete', index=idx)
    if err:
        Web.flash_error(httpResponse, err, ret, idx)
    else:
        err, ret = Web.command(httpResponse, 'save')
        msg = 'Gadget task deleted'
        httpResponse.FlashMessage(msg, 'info')

    return httpResponse.WriteResponseRedirect('/gadgets')

#######