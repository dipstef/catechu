import cPickle as pickle
import json
import sys

import web

urls = ('/cache/response', 'PageCacheResponse',
        '/cache', 'PageCacheContent')


app = web.application(urls, globals())


class PageCacheResponse(object):

    def GET(self):
        user_data = web.input()

        cache = caches.get_cache(**user_data)
        response = cache.get_response(user_data.url)

        return pickle.dumps(response) if response else ''

    def POST(self):
        user_data = web.input(_unicode=False)

        response = pickle.loads(user_data.response)

        cache = caches.get_cache(response.url, **user_data)
        cache.store(response)


class PageCacheContent(object):

    def GET(self):
        user_data = web.input()

        cache = caches.get_cache(**user_data)
        response = cache.get_response(user_data.url)

        if response:
            if bool(user_data.get('json')):
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


def serve(page_caches, port=8087):
    global caches
    caches = page_caches

    sys.argv = ['localhost']
    sys.argv.append(str(port))
    app.run()

    #After Keyboard Interrupt
    print 'Closing Caches'
    caches.close()
