from urlparse import urlparse

def resource_router(routes):
    """Given a dict of routes from resource_name: handler_func, return
    a dispatching router."""
    def handler(request):
        parse_result = urlparse(request.url)
        resource = parse_result.path.split('/')[1]
        if resource in routes:
            return routes[resource](request)
        else:
            return (404, [('Content-Type', 'text/html')], 'Not found')
    return handler

def method_router(routes):
    """Given a dict of routes from http_method: handler_func, return
    a dispatching router, e.g.

    {
        'GET': get_handler,
        'PUT': put_handler,
        'POST': post_handler,
        'DELETE': delete_handler,
    }
    """
    def handler(request):
        method = request.method
        return routes[method](request)
    return handler

def resource_method_router(routes):
    """Given a 2d dict of { resource_name: { http_method: handler_func } },
    return a dispatching router.

    Works by composing a resource router with a method router.

    Example:

        {
            'users': {
                'GET': users_get_handler,
            },
            'items': {
                'PUT': items_put_handler,
            },
        }
        """
    return resource_router({k:method_router(v) for k, v in routes.iteritems()})
