
from microWebSrv import MicroWebSrv

# ------------------------------------------------------------------------------

CONTENT_TEST = """\
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
"""

@MicroWebSrv.route('/test')
def _httpHandlerTestGet(httpClient, httpResponse) :
	
	content = CONTENT_TEST % httpClient.GetIPAddr()
	
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )

# ------------------------------------------------------------------------------

CONTENT_TEST_POST = """\
<!DOCTYPE html>
<html lang=en>
	<head>
		<meta charset="UTF-8" />
		<title>TEST POST</title>
	</head>
	<body>
		<h1>TEST POST</h1>
		Firstname = %s<br />
		Lastname = %s<br />
	</body>
</html>
"""

@MicroWebSrv.route('/test', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
	
	formData  = httpClient.ReadRequestPostedFormData()
	firstname = formData["firstname"]
	lastname  = formData["lastname"]
	
	content   = CONTENT_TEST_POST % ( 
		MicroWebSrv.HTMLEscape(firstname),
		MicroWebSrv.HTMLEscape(lastname) )
	
	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )

# ------------------------------------------------------------------------------

CONTENT_EDIT_TOP = """\
<!DOCTYPE html>
<html lang=en>
	<head>
		<meta charset="UTF-8" />
		<title>TEST EDIT</title>
	</head>
	<body>
"""
CONTENT_EDIT_BOTTOM = """
	</body>
</html>
"""

@MicroWebSrv.route('/edit/<index>')             # <IP>/edit/123           ->   args['index']=123
@MicroWebSrv.route('/edit/<index>/abc/<foo>')   # <IP>/edit/123/abc/bar   ->   args['index']=123  args['foo']='bar'
@MicroWebSrv.route('/edit')                     # <IP>/edit               ->   args={}
def _httpHandlerEditWithArgs(httpClient, httpResponse, args=None) :
	
	content = CONTENT_EDIT_TOP	
	
	if args:
		content += "<h1>EDIT item with {} variable arguments</h1>"\
			.format(len(args))
		if 'index' in args :
			content += "<p>index = {}</p>".format(args['index'])
		if 'foo' in args :
			content += "<p>foo = {}</p>".format(args['foo'])
		
	content += CONTENT_EDIT_BOTTOM

	httpResponse.WriteResponseOk( headers		 = None,
								  contentType	 = "text/html",
								  contentCharset = "UTF-8",
								  content 		 = content )

# ------------------------------------------------------------------------------

def _acceptWebSocketCallback(webSocket, httpClient) :
	print("WS ACCEPT")
	webSocket.RecvTextCallback   = _recvTextCallback
	webSocket.RecvBinaryCallback = _recvBinaryCallback
	webSocket.ClosedCallback 	 = _closedCallback

def _recvTextCallback(webSocket, msg) :
	print("WS RECV TEXT : %s" % msg)
	webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
	print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
	print("WS CLOSED")

# ------------------------------------------------------------------------------

#routeHandlers = [
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
#]

srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= False
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start(threaded=False)

# ------------------------------------------------------------------------------
