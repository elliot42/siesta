def response(status, headers, body):
    return (status, headers, body)

def html(status, body, headers=[]):
    return (status, [('Content-Type', 'text/html')], body)

def not_found(
        status=404,
        body="404 Not Found",
        headers=[('Content-Type', 'text/html')]):
    return response(status, headers, body)

def method_not_allowed(
        status=405,
        body="405 Method Not Allowed",
        headers=[('Content-Type', 'text/html')]):
    return response(status, headers, body)
