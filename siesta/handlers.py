def html_handler(request_handler):
    """Returns a handler, given a function that:
        takes a request, and returns HTML"""
    def handler(request):
        return (200, [('Content-type', 'text/html')], request_handler(request))
    return handler

def jinja_handler(template, data_provider):
    """Returns a request handler

    Requires a Jinja2 template, and a `data_provider` function
    that, given a request, returns a dict of bindings appropriate
    to fill in the template."""
    def handler(request):
        bindings = data_provider(request)
        return (200,
                [('Content-Type', 'text/html')],
                str(template.render(**bindings)))
    return handler
