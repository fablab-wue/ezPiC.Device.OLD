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

    ret.sort(key=lambda x: x['NAME'].upper())

    vars = {}
    vars['menu'] = 'gadgets'
    vars['gadget_list'] = ret

    return httpResponse.WriteResponsePyHTMLFile('web/www/gadgets.html', vars=vars)

#######

@MicroWebSrv.route('/gadgets/stage/')
def web_gadgets_list(httpClient, httpResponse):
    """ TODO """

    err, ret = Web.command(httpResponse, 'gadget.stage.list')
    if err:
        Web.flash_error(httpResponse, err, ret)
        ret = []

    ret.sort(key=lambda x: x['PNAME'].upper())

    vars = {}
    vars['menu'] = 'gadgets'
    vars['gadget_list'] = ret

    return httpResponse.WriteResponsePyHTMLFile('web/www/gadgets_list.html', vars=vars)

#######

@MicroWebSrv.route('/gadgets/add/<ezPID>/')
def web_gadget_add(httpClient, httpResponse, args):
    """ TODO """
    ezPID = args['ezPID']

    params = {'ezPID': ezPID}
    err, ret = Web.command(httpResponse, 'gadget.add', items=params)
    if err:
        Web.flash_error(httpResponse, err, ret, ezPID)
    else:
        Web.command(httpResponse, 'save')
        msg = 'Gadget "{}" added'.format(ezPID)
        httpResponse.FlashMessage(msg, 'info')
        return httpResponse.WriteResponseRedirect('/gadgets/edit/'+str(ret))

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
            params.update(formParams)
        err, ret = Web.command(httpResponse, 'gadget.setparams', index=idx, params=formParams)
        if not err:
            err, ret = Web.command(httpResponse, 'save')
        if err:
            Web.flash_error(httpResponse, err, ret, idx)
        else:
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
        err = ret.get('ERROR', None)
        if err:
            Web.flash_error(httpResponse, -999, err, idx)


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
        msg = 'Gadget instance deleted'
        httpResponse.FlashMessage(msg, 'info')

    return httpResponse.WriteResponseRedirect('/gadgets')

#######