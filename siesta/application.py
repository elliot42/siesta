from werkzeug.wrappers import Request, Response
from werkzeug.http import HTTP_STATUS_CODES

def application(application):
    def wsgi_application(environ, start_response):
        request = Request(environ)
        status_code, headers, body = application(request)
        status = ' '.join([str(status_code), HTTP_STATUS_CODES[status_code]])
        start_response(status, headers)
        return body
    return wsgi_application
