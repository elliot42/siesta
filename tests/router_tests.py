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
    router = routers.resource_router(TestResource)
    app = siesta.application.application(router)

    c = Client(app, BaseResponse)
    resp = c.post('/')
    assert resp.status_code == 200
