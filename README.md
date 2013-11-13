# siesta

`siesta` is a RESTful, functional web toolkit.  It's designed to give you
simple components, not giant incomprehensible frameworks.

## Example

```python
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

def simple_handler(request):
    return (200, [('Content-Type', 'text/html')], 'simple handler!')

router = siesta.routers.NestedResourceRouter(
    (IndexHandler(), {
        'cats': (CatsHandler(), {
            '*': CatHandler(),
        }),
        'dogs': (None, {
            '*': DogHandler()
        }),
        'meese': simple_handler,
    }))

app = siesta.application.application(router)

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, app)

# curl http://localhost:4000/cats/15
# => 'get cat!'
```

## Key Concepts

`siesta` is based on a few concepts:

1. The HTTP request-response cycle maps cleanly to functional programming (FP):
functions that take a request, and return a response.  The request handler
functions _compose_ into a pipeline that can express common operations such as
"check permissions before handling request."  FP handles all the guts of
servicing requests powerfully and concisely.

2. REST semantics are based on two minimal foundations: nouns (resources) and
verbs (methods).  While REST has many other important aspects (e.g. HATEOAS),
the vast majority of web services care primarily about making it easy to apply
methods to resources.  Therefore `siesta` provides as-obvious-as-possible
resource-oriented routing handlers out of the box, but allows you to implement
your own arbitrarily complex handlers should you truly need them.

3. The system should be based on a small set of explicitly composed tools,
not a magically conventional framework.
