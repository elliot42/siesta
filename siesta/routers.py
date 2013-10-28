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

def resource_descriptor_router(resource_handler_descriptor_klass):
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
    resource_handler_descriptor = resource_handler_descriptor_klass()
    routes = { method_name:getattr(resource_handler_descriptor, method_name.lower())
               for method_name
               in ['GET', 'PUT', 'POST', 'DELETE']
               if hasattr(resource_handler_descriptor, method_name.lower())
             }
    return method_router(routes)

class Resource:
    """Superclass/Mixin if you want to make your own Resource
    descriptor classes turn into routers easily.

    class MyResource(routers.Resource):
        def get(self, request):
            ...

    router = MyResource()
    """
    def __call__(self, request):
        router = resource_descriptor_router(self.__class__)
        return router(request)

class NestedResourceRouter:
    """Takes a route specification, and returns a handler that will
    route according to that specification.

    This breaks down a request URL by slash ('/') delimited:

    /
    /0.1.0
    /0.1.0/dogs
    /0.1.0/dogs/20

    And considers each path component a Resource, which can either
    be handled itself, or checked for if the request wants a child
    of the resource.

    Route specification is defined as either:

        resource_handler                   # Handler
        (resource_handler, child_handlers) # 2-typle of handler, children

    `child_handlers` is a `dict`:

        {
            <str:child_resource_name>: route_specification,
        }

    For example, a route specification looks like:

        (IndexHandler, {
             '0.1.0': (None, {
                 'dogs': (DogsHandler, {
                     '*': DogHandler,
                  })
             })
         })

    This guy is a callable; an instance acts like a function.
    """
    @classmethod
    def match_route(cls, path_list, routes):
        """Given a broken down path_component list from a request, and
        a routes specification, return the appropriate handler

        Example:

            routes = (IndexHandler, {
                 '0.1.0': (None, {
                     'dogs': (DogsHandler, {
                         '*': DogHandler,
                      })
                 })
             })

            path_list = ['0.1.0', 'dogs', '20']

            match_route(path_list, routes)
            # => DogHandler

        Complies with the basic rules specified above for route
        specifications.
        """

        # recusively advance down path_list, trying to match
        # up available routes against the resource currently
        # at the head of the path_list
        if len(path_list) == 0:
            # end of the path list; either what we're looking
            # for is here or it's not present at all.
            if routes:
                if type(routes) is not tuple:
                    return routes # routes is itself a handler
                elif type(routes) is tuple:
                    handler, child_handlers = routes
                    if handler:
                        return handler
            return handlers.passthrough(responses.not_found())
        else:
            # there are still items in the path list; the
            # request is for an item further down the `routes` tree;
            # try to find the next level deeper and recur.
            child_routes = routes[1]
            head, rest = path_list[0], path_list[1:]

            if head in child_routes:
                return cls.match_route(rest, child_routes[head])
            elif '*' in child_routes: # the wildcard route; matches anything.
                return cls.match_route(rest, child_routes['*'])
            return handlers.passthrough(responses.not_found())

    def __init__(self, routes):
        """Given a route specification, this router (self) up
        to find handlers according to the route specification."""
        self.routes = routes

    def __call__(self, request):
        """This object acts like a function, specifically a handler;
        When called with a request, it finds the appropriate handlers
        from its initial specification and then delegates generating
        the response to the found handler."""
        parse_result = urlparse(request.url)
        path_list = [p for p in parse_result.path.split('/') if p]
        resource_handler = self.match_route(path_list, self.routes)
        return resource_handler(request)
