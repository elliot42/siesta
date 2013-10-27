from urlparse import urlparse
from functools import partial
from siesta import handlers
from siesta import response as responses

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
        if method in routes:
            return routes[method](request)
        else:
            return handlers.passthrough(responses.method_not_allowed)(request)
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

def resource_router(resource_handler):
    """Given a class with `get`, `put`, `post`, `delete` methods,
    return a corresponding method router.

    This is just a slight bit of sugar over `method_router` that makes
    it easier to declare a set of methods on a resource, rather than
    having to deal with the dict literal syntax.

    Instead of:

        {
            'GET': get_handler, # hard to write this function inline;
            'PUT': put_handler, #   annoying to declare out-of-band
            ...
        }

    You get:

        class MyResource:
            def get(self, request):
                # ...
            def put(self, request):
                # ...

    which is a bit easier to work with.  But it just gets converted
    to the `method_router`
    """
    resource_handler_instance = resource_handler()
    routes = { method_name:getattr(resource_handler_instance, method_name.lower())
               for method_name
               in ['GET', 'PUT', 'POST', 'DELETE']
               if hasattr(resource_handler, method_name.lower())
             }
    return method_router(routes)
