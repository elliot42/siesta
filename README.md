# siesta

`siesta` is a RESTful, functional web toolkit.  It's designed to give you power
and clarity of your components, against the trend of sprawling,
incomprehensible and sugary one-size-fits-all frameworks.

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

`siesta` is based on a small number of powerful concepts:

1. The HTTP request-response cycle maps beautifully to functional programming
(FP).  All stages of request-to-response processing can be modeled as functions
that take a request, and return a response.  The request handler functions
_compose_ with each other into a pipeline that can express all our commonly
needed operations, such as "check permissions before handling request."  FP
handles all the guts of servicing requests powerfully and concisely.

2. REST semantics are based on two minimal foundations: nouns (resources) and
verbs (methods).  While REST has many other important aspects (e.g. HATEOAS),
the vast majority of web services care primarily about making it easy to apply
methods to resources.  Therefore `siesta` provides as-obvious-as-possible
resource-oriented routing handlers out of the box, but allows you to implement
your own arbitrarily complex handlers should you truly need them.

## Tenets

`siesta` is built on three mutually reinforcing tenets:

1. __Tools over frameworks__: build your app out of convenient interchangable
parts, not the procrustean bed of an all-encompassing framework.

2. __Explicit composition__: components are explicitly chained together so that
you can understand them, control them, and augment them.

3. __Minimal impedence mismatch__: components by default express themselves in
the most direct, immediate and obvious relation to their responsibility.
RESTful handlers are named directly for their HTTP verbs, not any other sugary
abstraction.  The persistence layer will NOT be an ORM, but will speak the
tuple language of the database itself.  This makes the system lean in both
concepts and code, but leaves open the options for as much layering as you like.

These three principles are designed to enable systems that are both powerful
and understandable, productive and fun.
