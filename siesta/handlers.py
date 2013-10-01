def html_handler(request_handler):
    """Returns a handler, given a function that:
        takes a request, and returns HTML"""
    def handler(request):
        return (200, [('Content-type', 'text/html')], request_handler(request))
    return handler
