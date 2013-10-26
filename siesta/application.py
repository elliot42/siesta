from werkzeug.wrappers import Request, Response
from werkzeug.http import HTTP_STATUS_CODES

def application(application):
    def wsgi_application(environ, start_response):
        request = Request(environ)
        status_code, headers, body = application(request)
        response = Response(body, status=status_code, headers=headers)
        return response(environ, start_response)
    return wsgi_application
