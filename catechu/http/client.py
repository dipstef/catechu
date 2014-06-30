import cPickle as pickle
from httpy import HttpResponse, httpy

from urlo.unquoted import build_url


class CacheClient(object):

    def __init__(self, address, path='/cache/response', client=httpy):
        self._client = client
        self._url = build_url(host=address[0], port=address[1], path=path)

    def store(self, response):
        response = HttpResponse(response.request, response.url, response.status, response.headers, response.body)
        response_string = pickle.dumps(response)

        return self._client.post(self._url, data={'response': response_string}, timeout=None)

    def get_response(self, url):
        response = self._client.get(self._url, timeout=None, params={'url': url})
        if response.body:
            return pickle.loads(response.body)