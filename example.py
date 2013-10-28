import siesta.application
import siesta.routers

class IndexHandler(siesta.routers.Resource):
    def get(self, request):
        return (200, [('Content-Type', 'text/html')], 'index!')

class CatsHandler(siesta.routers.Resource):
    def get(self, request):
        return (200, [('Content-Type', 'text/html')], 'collection of cats!')

class CatHandler(siesta.routers.Resource):
    def get(self, request):
        return (200, [('Content-Type', 'text/html')], 'get cat!')

    def put(self, request):
        return (200, [('Content-Type', 'text/html')], 'put cat!')

class DogHandler(siesta.routers.Resource):
    def get(self, request):
        return (200, [('Content-Type', 'text/html')], 'get dog!')

router = siesta.routers.NestedResourceRouter(
    (IndexHandler(), {
        'cats': (CatsHandler(), {
            '*': CatHandler(),
        }),
        'dogs': (None, {
            '*': DogHandler()
        }),
    }))

app = siesta.application.application(router)

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, app)

# curl http://localhost:4000/cats/15
# => 'one cat!'
