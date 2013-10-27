def response(status, headers, body):
    return (status, headers, body)

def html(status, body, headers=[]):
    return (status, [('Content-Type', 'text/html')], body)

def not_found(
        status=404,
        body="404 Not Found",
        headers=[('Content-Type', 'text/html')]):
    return response(status, headers, body)

method_not_allowed = (
    405, 
    [('Content-Type', 'text/html')],
    "405 Method Not Allowed")

ok = (200, [('Content-Type', 'text/html')], '200 OK')
