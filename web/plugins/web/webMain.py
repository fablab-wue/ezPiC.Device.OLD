"""
Web Plugin for Index-Page and Main-Page
"""
from com.Globals import *

from web.MicroWebSrv.microWebSrv import MicroWebSrv
import web.Web as Web

#######

@MicroWebSrv.route('/')
def web_index(httpClient, httpResponse):
    """ Index-Page with Description. Additional handle commands over HTTP-GET"""
    queryParams = httpClient.GetRequestQueryParams()
    if queryParams and 'cmd' in queryParams:
        cmd = queryParams.get('cmd')
        err, ret = Web.command(httpResponse, cmd)
        json = {'code': err, 'result': ret}
        return httpResponse.WriteResponseJSONOk(json)

    vars = {}
    vars['menu'] = ''

    return httpResponse.WriteResponsePyHTMLFile('web/www/index.html', vars=vars)

#######

#@APP.errorhandler(404)
#def web_error(error):
#    """ TODO """
#    return render_template('error.html', error=error), 404

#######

@MicroWebSrv.route('/main')
def web_main(httpClient, httpResponse):
    """ Main-Page with common dashboard """
    
    err, result = Web.command(httpResponse, 'info')
    if err:
        Web.flash_error(httpResponse, err, result)
        result = {}

    vars = {}
    vars['menu'] = 'main'
    vars['info'] = result

    return httpResponse.WriteResponsePyHTMLFile('web/www/main.html', vars=vars)

#######

@MicroWebSrv.route('/test')
def _httpHandlerTestGet(httpClient, httpResponse) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>TEST GET</title>
        </head>
        <body>
            <h1>TEST GET</h1>
            Client IP address = %s
            <br />
			<form action="/test" method="post" accept-charset="ISO-8859-1">
				First name: <input type="text" name="firstname"><br />
				Last name: <input type="text" name="lastname"><br />
				<input type="submit" value="Submit">
			</form>
        </body>
    </html>
	""" % httpClient.GetIPAddr()
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )

#######