from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

import siesta.application
from siesta import routers
from siesta import response as responses
from siesta import handlers

def test_method_router_method_ok():
    """Tests that a `method_router` can find a handler by HTTP method
    successfully."""
    routes = {
        'GET': siesta.handlers.passthrough(responses.ok),
    }
    router = routers.method_router(routes)
    app = siesta.application.application(router)
    c = Client(app, BaseResponse)
    resp = c.get('/')
    assert resp.status_code == 200

def test_method_router_method_not_allowed():
    """Tests that `method_router` returns 405 Method Not Allowed
    when requested with a method it doesn't have."""
    routes = {
        'GET': handlers.passthrough(responses.ok),
    }
    router = routers.method_router(routes)
    app = siesta.application.application(router)
    c = Client(app, BaseResponse)
    resp = c.post('/')
    assert resp.status_code == 405

def test_resource_descriptor_router_get_found_status():
    class TestResource:
        def get(self, request):
            return responses.ok
    router = routers.resource_descriptor_router(TestResource)
    app = siesta.application.application(router)
    c = Client(app, BaseResponse)
    resp = c.get('/')
    assert resp.status_code == 200

def test_resource_descriptor_router_get_found_content():
    class TestResource:
        def get(self, request):
            return responses.ok
    router = routers.resource_descriptor_router(TestResource)
    app = siesta.application.application(router)

    c = Client(app, BaseResponse)
    resp = c.get('/')
    assert ''.join(resp.response) == responses.ok[2]

def test_resource_descriptor_router_method_not_allowed_status():
    class TestResource:
        def get(self, request):
            return responses.ok
    router = routers.resource_descriptor_router(TestResource)
    app = siesta.application.application(router)
    c = Client(app, BaseResponse)
    resp = c.post('/')
    assert resp.status_code == 405

def test_resource_descriptor_router_post():
    class TestResource:
        def post(self, request):
            return responses.ok
    router = routers.resource_descriptor_router(TestResource)
    app = siesta.application.application(router)

    c = Client(app, BaseResponse)
    resp = c.post('/')
    assert resp.status_code == 200

def test_nested_resource_router_root():
    """Test that it hits the root handler"""
    index_handler = handlers.passthrough(responses.ok)
    ok = handlers.passthrough(responses.ok)

    routes = (index_handler, {
                  '0.1.0': (None, {
                      'dogs': (ok, {
                          '*': ok,
                       })
                  })
              })

    router = routers.NestedResourceRouter(routes)
    app = siesta.application.application(router)

    c = Client(app, BaseResponse)
    resp = c.post('/')
    assert resp.status_code == 200

def test_nested_resource_router_nested_resource():
    "Test that it can hit a nested resource"""
    index_handler = handlers.passthrough(responses.ok)
    dogs_handler = handlers.html_handler(lambda request: 'dogs!')
    dog_handler = handlers.html_handler(lambda request: 'holla!')

    routes = (index_handler, {
                  '0.1.0': (None, {
                      'dogs': (dogs_handler, {
                          '*': dog_handler,
                       })
                  })
              })

    router = routers.NestedResourceRouter(routes)
    app = siesta.application.application(router)

    c = Client(app, BaseResponse)
    resp = c.post('/0.1.0/dogs')
    assert ''.join(resp.response) == 'dogs!'

def test_nested_resource_router_proper_nested_resource():
    """Test that it can hit a proper nested resource, choosing
    between several available at the level"""
    def html_passthrough_handler(content):
        return handlers.html_handler(lambda request: content)

    dogs_handler = html_passthrough_handler('dogs!')
    cats_handler = html_passthrough_handler('cats!')
    hogs_handler = html_passthrough_handler('hogs!')

    routes = (None, {
                  '0.1.0': (None, {
                      'dogs': dogs_handler,
                      'cats': cats_handler,
                      'hogs': hogs_handler,
                  })
              })

    router = routers.NestedResourceRouter(routes)
    app = siesta.application.application(router)

    c = Client(app, BaseResponse)
    resp = c.post('/0.1.0/cats')
    assert ''.join(resp.response) == 'cats!'


def test_nested_resource_router_wildcard_resource():
    "Test that it can hit a wildcard resource"""
    index_handler = handlers.passthrough(responses.ok)
    dogs_handler = handlers.html_handler(lambda request: 'dogs!')
    dog_handler = handlers.html_handler(lambda request: 'holla!')

    routes = (index_handler, {
                  '0.1.0': (None, {
                      'dogs': (dogs_handler, {
                          '*': dog_handler,
                       })
                  })
              })

    router = routers.NestedResourceRouter(routes)
    app = siesta.application.application(router)

    c = Client(app, BaseResponse)
    resp = c.post('/0.1.0/dogs/20')
    assert ''.join(resp.response) == 'holla!'

def test_nested_resource_router_404_no_route():
    "Test that it 404s on a missing route"""
    index_handler = handlers.passthrough(responses.ok)
    dogs_handler = handlers.passthrough(responses.ok)
    dog_handler = handlers.html_handler(lambda request: 'holla!')

    routes = (index_handler, {
                  '0.1.0': (None, {
                      'dogs': (dogs_handler, {
                          '*': dog_handler,
                       })
                  })
              })

    router = routers.NestedResourceRouter(routes)
    app = siesta.application.application(router)

    c = Client(app, BaseResponse)
    resp = c.post('/0.1.0/cats')
    assert resp.status_code == 404

def test_nested_resource_router_404_none_route():
    "Test that it 404s on a None route"""
    index_handler = handlers.passthrough(responses.ok)
    dogs_handler = handlers.passthrough(responses.ok)
    dog_handler = handlers.html_handler(lambda request: 'holla!')

    routes = (index_handler, {
                  '0.1.0': (None, {
                      'dogs': (dogs_handler, {
                          '*': dog_handler,
                       })
                  })
              })

    router = routers.NestedResourceRouter(routes)
    app = siesta.application.application(router)

    c = Client(app, BaseResponse)
    resp = c.post('/0.1.0')
    assert resp.status_code == 404

def test_nested_resource_router_subwildcard():
    "Test that it can hit a named route beneath a wildcard"""

    ok = handlers.passthrough(responses.ok)

    routes = (None, {
                 '0.1.0': (None, {
                      'dogs': (None, {
                          '*': (None, {
                              'fur': ok,
                          }),
                      })
                  })
             })

    router = routers.NestedResourceRouter(routes)
    app = siesta.application.application(router)

    c = Client(app, BaseResponse)
    resp = c.post('/0.1.0/dogs/40/fur')
    assert resp.status_code == 200
