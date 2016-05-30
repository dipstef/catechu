import cPickle as pickle
import inspect
import json

from bottle import Bottle, BaseRequest, request

app = Bottle()


@app.get('/cache/response')
def get_response(caches):
    cache = caches.get_cache(**request.query)
    response = cache.get_response(request.GET['url'])

    return pickle.dumps(response) if response else ''


@app.post('/cache/response')
def save_response(caches):
    cache = caches.get_cache(**request.query)
    response = pickle.loads(request.POST['response'])

    cache.store(response)


@app.get('/cache')
def get_content(caches):
    cache = caches.get_cache(**request.query)
    response = cache.get_response(request.GET['url'])

    if response:
        if bool(request.GET['json']):
            return json.dumps(_response_dict(response))
        return response.body


def _response_dict(response):
    request = response.request
    return {'request': {'url': request.url,
                        'method': request.method},
            'url': response.url,
            'headers': dict(response.headers),
            'status': response.status,
            'body': response.body}


class BottlePlugin(object):
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def apply(self, callback, context):
        """Return a decorated route callback."""
        args = inspect.getargspec(context['callback'])[0]
        # Skip this callback if we don't need to do anything

        keywords = {k: v for k, v in self._kwargs.iteritems() if k in args}

        if not keywords:
            return callback

        def wrapper(*a, **ka):
            ka.update(keywords)
            rv = callback(*a, **ka)
            return rv

        return wrapper

    def __str__(self):
        components = '\n'.join(('{component} (keyword={keyword})'.format(component=component,
                                                                         keyword=keyword)
                                for keyword, component in self._kwargs.iteritems()))

        return '{klass} using:\n{components})'.format(klass=self.__class__.__name__,
                                                      components=components)

    def __repr__(self):
        return str(self)


class CachesPlugin(BottlePlugin):
    def __init__(self, caches, keyword='caches'):
        """ :param keyword: """
        super(CachesPlugin, self).__init__(**{keyword: caches})
        self._caches = caches

    def close(self):
        print 'Closing Caches'
        self._caches.close()


def serve(page_caches, port=8087, body_max_mb=100):
    BaseRequest.MEMFILE_MAX = body_max_mb * 2 ** 20

    plugin = CachesPlugin(page_caches)
    app.install(plugin)

    app.run(port=port)
