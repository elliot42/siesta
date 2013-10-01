import siesta.application
import siesta.routers
from siesta.handlers import html_handler as handle

router = siesta.routers.resource_method_router({
    '': { 'GET': handle(lambda request: 'Hello world!') },
    'cats' : {
        'GET': handle(lambda request: 'Cat GET!!!'),
        'PUT': handle(lambda request: 'CAT PUT!!!'),
    },
    'dogs' : {},
})

app = siesta.application.application(router)

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, app)
