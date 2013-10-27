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
