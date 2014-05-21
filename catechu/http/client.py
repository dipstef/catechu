import cPickle as pickle
from httpy.client import http_client

from httpy.response import HttpResponse
from urlo.parser import build_url


class CacheClient(object):

    def __init__(self, address, path='/cache/response', client=http_client):
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